import os
from dotenv import load_dotenv
load_dotenv()

from app.db.pg_vector_store import PGVectorStore
from app.llm_providers.api_client import get_llm_client

vector_store = PGVectorStore()
llm = get_llm_client()


def normalize_query(q: str) -> str:
    return q.lower().strip().replace("?", "").replace(".", "")


def get_embedding(text: str):
    """Generates embedding using the configured LLM client."""
    return llm.embed(text)


def get_best_match(
    query: str,
    collection1: str = "yoga_collection",
    collection2: str = "gita_collection",
    limit: int = 1
):
    query_norm = normalize_query(query)
    query_embedding = get_embedding(query_norm)

    # 1️⃣ Search both collections (FIXED METHOD)
    results1 = vector_store.search_knowledge(
        embedding=query_embedding,
        table=collection1,
        top_k=limit
    )

    results2 = vector_store.search_knowledge(
        embedding=query_embedding,
        table=collection2,
        top_k=limit
    )

    # 2️⃣ Extract distances safely
    dist1 = results1[0].get('distance', 1.0) if results1 else 1.0
    dist2 = results2[0].get('distance', 1.0) if results2 else 1.0

    # 3️⃣ Convert distance to similarity score
    score1 = 1 / (1 + dist1)
    score2 = 1 / (1 + dist2)

    print(f"DEBUG: {collection1} Similarity: {score1:.4f}")
    print(f"DEBUG: {collection2} Similarity: {score2:.4f}")

    # 4️⃣ KEYWORD OVERRIDE (Hard Routing)
    gita_keywords = ["krishna", "arjuna", "geeta", "gita", "kurukshetra", "pandava", "dharma"]
    yoga_keywords = ["patanjali", "sutra", "asana", "pranayama", "limbs", "niyama", "eight"]

    if any(kw in query_norm for kw in gita_keywords):
        return collection2

    if any(kw in query_norm for kw in yoga_keywords):
        return collection1

    # 5️⃣ SEMANTIC ROUTING
    if score1 > 0.5 or score2 > 0.5:
        return collection1 if score1 >= score2 else collection2

    # 6️⃣ Final fallback
    return collection2 if query_norm.count("gita") >= query_norm.count("yoga") else collection1

