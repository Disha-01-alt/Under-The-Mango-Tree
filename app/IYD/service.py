import json
import logging
from app.IYD import pipeline_logic as rag
from app.llm_providers.api_client import get_llm_client
from app.inference.retrieve_cache import store_context_cache

# Initialize the unified LLM client
llm = get_llm_client()

# Initialize the Verifier logic
verifier = rag.ClaimVerifier(llm_provider=llm)

logger = logging.getLogger(__name__)

def verify_claim_service(statement: str, user_id: str) -> dict:
    original_query = statement
    query = rag.normalize(statement)

    # 1. Retrieve candidates
    faiss_ranks = rag.get_faiss_ranks(query, 10)
    bm25_ranks = rag.get_bm25_ranks(query, 10)

    # 2. Handle "Not Related" case
    if not faiss_ranks:
        result = {
            "relevance": "NOT_RAMAYANA_RELATED",
            "prediction": "NOT RELEVANT",
            "explanation": "No relevant verses found in Valmiki Ramayana to support or refute this claim.",
            "confidence": 0,
            "verses": [],
            "youtube_link": None,
            "download_link": None
        }
        store_context_cache(original_query, "Not relevant", result["explanation"], [], "IYD", user_id)
        return result

    # 3. Hybrid Retrieval (Reciprocal Rank Fusion)
    # FIXED: Changed parameter name from top_n to top_k
    retriever = rag.EnsembleRetriever([faiss_ranks, bm25_ranks])
    retrieved_verses = retriever.retrieve(top_k=10) 

    # 4. Cross-encoder reranking 
    # (Using a pass-through since we are using high-quality embeddings/API)
    top_verses = retrieved_verses[:5]

    # 5. LLM Verification
    try:
        # FIXED: verify_claim now returns the DICT directly, no need to parse again
        processed_json = verifier.verify_claim(query, top_verses)
        
        # 6. Post-processing & Reference Mapping
        processed_json = rag.extract_ref(processed_json, top_verses)
        
        # Ensure explanation exists
        final_explanation = processed_json.get("explanation", "No explanation provided.")

        final_result = {
            "relevance": processed_json.get("relevance", "RAMAYANA_RELATED"),
            "prediction": processed_json.get("label", "UNKNOWN"),
            "explanation": final_explanation,
            "confidence": processed_json.get("confidence_score", 0),
            "verses": top_verses,
            "youtube_link": None,
            "download_link": None
        }
    except Exception as e:
        logger.error(f"IYD Verification failed: {e}")
        return {"error": f"Failed to verify claim: {str(e)}"}

    # 7. Store in Cache
    store_context_cache(
        query=original_query,
        summary_answer=f"Claim is {final_result['prediction']}",
        detailed_answer=final_result["explanation"],
        references=top_verses,
        mode="IYD",
        user_id=user_id
    )

    return final_result
