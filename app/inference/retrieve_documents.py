from app.db.pg_vector_store import PGVectorStore
from app.llm_providers.api_client import get_llm_client

vector_store = PGVectorStore()
llm = get_llm_client()


def normalize_query(q: str) -> str:
    """
    Standardizes query text to match the normalization 
    used in the Cache and Vector Store.
    """
    return (
        q.lower()
        .strip()
        .replace("?", "")
        .replace(".", "")
        .replace(",", "")
    )


def retrieve_context(query: str, collection: str, limit: int = 4):
    """
    STEP 2: Retrieve RAW scripture rows from DB.

    - No LLM generation here.
    - No summarization.
    - Returns DB-authoritative fields (chapter, verse, sanskrit, links, etc).
    """

    # 1. Normalize query to generate a high-quality embedding
    query_norm = normalize_query(query)
    embedding = llm.embed(query_norm)

    # 2. Perform Vector Search (Cosine Similarity)
    # The result objects already contain 'youtube_link' and 'download_link' 
    # as defined in pg_vector_store.py formatting.
    results = vector_store.search_knowledge(
        embedding=embedding,
        table=collection,
        top_k=limit
    )

    # 3. Clean and return results
    # Each result in the list is a dictionary representing a row in Postgres.
    # Structure example:
    # {
    #   "id": 101, 
    #   "chapter": "2", 
    #   "verse": "47", 
    #   "sanskrit": "...", 
    #   "youtube_link": "...", 
    #   "download_link": "...", 
    #   "distance": 0.12
    # }
    return results
