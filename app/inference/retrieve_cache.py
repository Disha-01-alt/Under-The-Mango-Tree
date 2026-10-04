import json
import math
import logging
from app.db.pg_vector_store import PGVectorStore
from app.llm_providers.api_client import get_llm_client

logger = logging.getLogger(__name__)
vector_store = PGVectorStore()
llm = get_llm_client()

def normalize_query(q: str) -> str:
    """Standardizes the string for exact matching."""
    return (
        q.lower()
        .strip()
        .replace("?", "")
        .replace(".", "")
        .replace(",", "")
    )

def sanitize_metadata(data):
    """Recursively replaces NaN with 0.0 to prevent Postgres JSONB crashes."""
    if isinstance(data, dict):
        return {k: sanitize_metadata(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_metadata(x) for x in data]
    elif isinstance(data, float):
        if math.isnan(data) or math.isinf(data):
            return 0.0
        return data
    return data

def retrieve_context_cache(query: str, mode: str, user_id: str):
    normalized_q = normalize_query(query)

    # 1️⃣ CHECK USER CACHE (Exact Match)
    user_hit = vector_store.get_exact_cache(normalized_q, mode, user_id)
    if user_hit:
        return _format_cache_response(user_hit, "cache_user_exact")

    # 2️⃣ CHECK GLOBAL CACHE (Exact Match)
    with vector_store.conn.cursor() as cur:
        cur.execute(
            """
            SELECT summary_answer, detailed_answer, youtube_link, download_link, metadata, embedding
            FROM qna_collection
            WHERE mode = %s AND normalized_question = %s AND user_id IS NULL
            LIMIT 1;
            """,
            (mode, normalized_q),
        )
        row = cur.fetchone()

    if row:
        summary, detailed, yt, dl, metadata, existing_embedding = row
        parsed_refs = _parse_metadata(metadata)
        
        # 🔐 Propagate GLOBAL → USER (Optimized: reuse existing_embedding)
        if user_id:
            try:
                if not vector_store.question_exists(mode, normalized_q, user_id):
                    vector_store.insert_qna_cache(
                        embedding=existing_embedding, # Reuse to save API quota
                        question=normalized_q,
                        summary=summary,
                        detailed=detailed,
                        youtube_link=yt,
                        download_link=dl,
                        mode=mode,
                        metadata=parsed_refs,
                        user_id=user_id
                    )
            except Exception as e:
                logger.error(f"Failed to propagate global cache to user: {e}")

        return {
            "summary_answer": summary,
            "detailed_answer": detailed,
            "youtube_link": yt,
            "download_link": dl,
            "references": parsed_refs,
            "source": "cache_global_exact",
        }

    return None

def store_context_cache(
    query: str,
    summary_answer: str,
    detailed_answer: str,
    references: list,
    mode: str,
    user_id: str,
    youtube_link: str = None,
    download_link: str = None,
):
    normalized_q = normalize_query(query)
    
    # Clean the references (metadata) to remove any NaN values from similarity scores
    clean_references = sanitize_metadata(references)

    # Generate embedding (with internal retries inside LLMClient)
    embedding = llm.embed(normalized_q)
    
    # Validation: If embedding failed, LLMClient returns 0.0 vector. 
    # We allow it so exact-match still works, but log it.
    if sum(map(abs, embedding)) == 0:
        logger.warning(f"Storing cache for '{normalized_q}' with zero-vector due to embedding failure.")

    # Insert into Global
    if not vector_store.question_exists(mode=mode, normalized_question=normalized_q, user_id=None):
        try:
            vector_store.insert_qna_cache(
                embedding=embedding,
                question=normalized_q,
                summary=summary_answer,
                detailed=detailed_answer,
                youtube_link=youtube_link,
                download_link=download_link,
                mode=mode,
                metadata=clean_references,
                user_id=None
            )
        except Exception as e:
            logger.error(f"Error saving global cache: {e}")

    # Insert into User
    if user_id and not vector_store.question_exists(mode=mode, normalized_question=normalized_q, user_id=user_id):
        try:
            vector_store.insert_qna_cache(
                embedding=embedding,
                question=normalized_q,
                summary=summary_answer,
                detailed=detailed_answer,
                youtube_link=youtube_link,
                download_link=download_link,
                mode=mode,
                metadata=clean_references,
                user_id=user_id
            )
        except Exception as e:
            logger.error(f"Error saving user cache: {e}")

def _format_cache_response(hit, source):
    return {
        "summary_answer": hit["summary_answer"],
        "detailed_answer": hit["detailed_answer"],
        "youtube_link": hit.get("youtube_link"),
        "download_link": hit.get("download_link"),
        "references": _parse_metadata(hit["metadata"]),
        "source": source
    }

def _parse_metadata(metadata):
    if not metadata: return []
    if isinstance(metadata, str):
        try:
            return json.loads(metadata)
        except:
            return []
    if isinstance(metadata, dict):
        return [metadata]
    return metadata
