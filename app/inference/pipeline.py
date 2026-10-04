import re
import sys
import math # Added for NaN check
from dotenv import load_dotenv

sys.path.append("..")

from app.inference.retrieve_cache import store_context_cache
from app.inference.retrieve_documents import retrieve_context
from app.inference.query_filter import check_offensive_language, check_valid
from app.inference.response_gen import get_bot_response
from app.inference.find_correct_collection import get_best_match

load_dotenv()

# --- HELPER TO PREVENT DB CRASH ---
def sanitize_results(results):
    """Ensures no NaN values are passed to Postgres JSONB."""
    for r in results:
        if "distance" in r:
            if math.isnan(r["distance"]) or math.isinf(r["distance"]):
                r["distance"] = 0.99  # Safe default for 'not very similar'
        # Optional: Remove embedding from results to save space in QnA cache
        if "embedding" in r:
            del r["embedding"]
    return results

def normalize_query(q: str) -> str:
    return q.lower().strip().replace("?", "").replace(".", "").replace(",", "")

def is_small_talk(query: str) -> bool:
    # (Your existing regex patterns are fine)
    patterns = [r'^(hi|hey|hello|howdy)[\s!]*$', r'^how are you[\s?!]*$', r'^thanks[\s!]*$'] 
    return any(re.match(p, query) for p in patterns)

def get_small_talk_response():
    return {
        "summary_answer": "🙏 Namaste",
        "detailed_answer": (
            "I answer questions using the **Bhagavad Gita**, "
            "**Patanjali Yoga Sutras**, and **Valmiki Ramayana**.\n\n" # Added Ramayana
            "Ask me about karma, dharma, or the life of Sri Rama."
        ),
        "references": [], "youtube_link": None, "download_link": None
    }

def verse_is_irrelevant(llm_answer: dict) -> bool:
    if not llm_answer: return True
    text = (llm_answer.get("summary_answer", "") + llm_answer.get("detailed_answer", "")).lower()
    rejection_phrases = ["not mentioned", "not discussed", "outside this scripture", "not related to this verse"]
    return any(p in text for p in rejection_phrases)

def pipeline_rag_cache(query: str, mode: str, user_id: str):
    query_norm = normalize_query(query)

    # 0️⃣ Guardrails
    if check_offensive_language(query_norm) == 1:
        return {"summary_answer": "Invalid Query", "detailed_answer": "Please ask scriptural or spiritual questions.", "references": []}

    # 1️⃣ Small talk
    if is_small_talk(query_norm):
        response = get_small_talk_response()
        store_context_cache(query=query_norm, summary_answer=response["summary_answer"], 
                            detailed_answer=response["detailed_answer"], references=[], 
                            mode=mode, user_id=user_id)
        return response

    if check_valid(query_norm) == 1:
        return {
            "summary_answer": "Focus: Vedic Wisdom",
            "detailed_answer": "I am specialized in the Gita, Yoga Sutras, and Ramayana. Please ask a related question.",
            "references": []
        }

    # 2️⃣ Knowledge retrieval
    collection = get_best_match(query_norm)
    results = retrieve_context(query_norm, collection, limit=2)
    
    # --- CRITICAL FIX: Sanitize the results to remove NaN ---
    results = sanitize_results(results)

    # 3️⃣ No scripture found or Distance too high → LLM only
    if not results or results[0].get("distance", 1.0) >= 0.85: # Adjusted threshold
        llm_answer = get_bot_response(question=query_norm, row=None) or {}
        summary = llm_answer.get("summary_answer", "General Knowledge Answer")
        detailed = "⚠️ **No specific verse found. This is based on general scriptural knowledge.**\n\n" + llm_answer.get("detailed_answer", "")

        store_context_cache(query=query_norm, summary_answer=summary, detailed_answer=detailed, 
                            references=[], mode=mode, user_id=user_id)
        return {"summary_answer": summary, "detailed_answer": detailed, "references": []}

    # 4️⃣ Scripture grounded answer
    best_row = results[0]
    llm_answer = get_bot_response(question=query_norm, row=best_row) or {}

    yt_link = best_row.get("youtube_link")
    dl_link = best_row.get("download_link")

    # 5️⃣ Verify if LLM rejected the verse as irrelevant
    if verse_is_irrelevant(llm_answer):
        # Instead of calling API again, just modify the existing answer or use a generic one
        summary = "General Guidance"
        detailed = "⚠️ **The closest verses found were not directly related. Here is general guidance:**\n\n" + llm_answer.get("detailed_answer", "")
        
        store_context_cache(query=query_norm, summary_answer=summary, detailed_answer=detailed, 
                            references=[], mode=mode, user_id=user_id)
        return {"summary_answer": summary, "detailed_answer": detailed, "references": []}

    # 6️⃣ SUCCESS: Valid scripture answer
    summary = llm_answer.get("summary_answer")
    detailed = llm_answer.get("detailed_answer")

    store_context_cache(
        query=query_norm, summary_answer=summary, detailed_answer=detailed,
        references=[best_row], mode=mode, user_id=user_id,
        youtube_link=yt_link, download_link=dl_link
    )

    return {
        "summary_answer": summary,
        "detailed_answer": detailed,
        "references": [best_row],
        "youtube_link": yt_link,
        "download_link": dl_link
    }
