import os
import re
import json
import unicodedata
import logging
from app.llm_providers.api_client import get_llm_client
from app.db.pg_vector_store import PGVectorStore

logger = logging.getLogger(__name__)

# Shared instances (API based)
llm = get_llm_client()
store = PGVectorStore()

VARIANT_MAP = {
    "seetha": "sita", "seeta": "sita", "maithili": "sita", "janaki": "sita", "vaidehi": "sita",
    "ram": "rama", "raghava": "rama", "hanuma": "hanuman", "lakshman": "lakshmana"
}

def normalize(text):
    if not text: return ""
    text = unicodedata.normalize("NFKC", text).encode('ASCII', 'ignore').decode('utf-8')
    text = text.lower()
    text = re.sub(r"[^\w\s'.,/\-:;?!\()]", "", text)
    for variant, canonical in VARIANT_MAP.items():
        pattern = re.compile(fr"\b{variant}\b", flags=re.IGNORECASE)
        text = pattern.sub(canonical, text)
    return text.strip()

# --- RETRIEVAL HELPERS ---

def get_faiss_ranks(query, top_k=10):
    """Replaces local FAISS with Postgres Vector Search"""
    embedding = llm.embed(query)
    # Search specifically in the ramayana_collection table
    return store.search_knowledge(embedding, "ramayana_collection", top_k=top_k)

def get_bm25_ranks(query, top_k=10): 
    # Optional: If you haven't implemented BM25 in Postgres yet, return empty
    # This ensures the EnsembleRetriever still has a list to work with
    return [] 

# --- NEW: ENSEMBLE RETRIEVER (Fixed the missing class) ---

class EnsembleRetriever:
    def __init__(self, retrievers, weights=None):
        """
        Combines results from multiple retrievers (FAISS/BM25).
        """
        self.retrievers = retrievers
        self.weights = weights or [1.0 / len(retrievers)] * len(retrievers)

    def retrieve(self, top_k=5):
        """
        Merges results using simple ranking.
        """
        all_results = {}
        for i, hits in enumerate(self.retrievers):
            weight = self.weights[i]
            for rank, hit in enumerate(hits):
                # Unique key: Chapter + Verse + Translation snippet
                content_key = f"{hit.get('chapter')}_{hit.get('verse')}"
                
                score = weight * (1.0 / (rank + 60)) # Reciprocal Rank Fusion
                
                if content_key in all_results:
                    all_results[content_key]["ensemble_score"] += score
                else:
                    hit["ensemble_score"] = score
                    all_results[content_key] = hit

        sorted_hits = sorted(all_results.values(), key=lambda x: x["ensemble_score"], reverse=True)
        return sorted_hits[:top_k]

# --- CLAIM VERIFIER ---

class ClaimVerifier:
    def __init__(self, llm_provider):
        self.llm = llm_provider

    def build_system_prompt(self):
        return """
        You are a scholarly expert in the Valmiki Ramayana. Your task is to fact-check a claim using ONLY the provided textual evidence.
        
        Output EXACTLY this JSON format:
        {
          "relevance": "RAMAYANA_RELATED" or "NOT_RAMAYANA_RELATED",
          "label": "TRUE" or "FALSE",
          "confidence_score": 1-10,
          "reference": [list of numbers],
          "explanation": "Brief reasoning."
        }
        Guidelines:
        1. If the evidence supports the claim, label is TRUE.
        2. If the evidence contradicts it, label is FALSE.
        3. If evidence is missing or insufficient, label is FALSE.
        """

    def verify_claim(self, claim, verses):
        verses_text = "\n".join([f"{i}. [{v.get('chapter')}, Verse {v.get('verse')}] {v['translation']}" for i, v in enumerate(verses, 1)])
        system_prompt = self.build_system_prompt()
        user_prompt = f"**CLAIM:**\n{claim}\n\n**TEXTUAL EVIDENCE:**\n{verses_text}\n\nOutput only the JSON."
        
        raw_response = self.llm.generate_response(system_prompt, user_prompt)
        return extract_fact_check_json(raw_response)

# --- POST-PROCESSING ---

def extract_fact_check_json(text):
    try:
        match = re.search(r'\{[\s\S]*\}', text)
        if not match: return {"label": "UNKNOWN", "explanation": "Invalid LLM Output"}
        return json.loads(match.group(0))
    except Exception as e:
        logger.error(f"JSON Parsing Error: {e}")
        return {"label": "UNKNOWN", "explanation": f"Parsing error: {str(e)}"}

def extract_ref(json_data, top_verses):
    """Converts index numbers like [1] to 'Bala Kanda, Verse 5'"""
    if not json_data.get('reference'): return json_data
    
    updated_refs = []
    for s in json_data['reference']:
        try:
            idx = int(s)
            if 1 <= idx <= len(top_verses):
                meta = top_verses[idx-1]
                # Match the column names from your PGVectorStore
                formatted = f"{meta.get('chapter', 'Unknown')}, Verse {meta.get('verse', 'N/A')}"
                updated_refs.append(formatted)
        except:
            continue
    
    json_data['reference'] = list(set(updated_refs)) # Remove duplicates
    return json_data

# --- THE MAIN PIPELINE FUNCTION ---

def run_iyd_pipeline(statement):
    """
    This is the main function called by service.py
    """
    # 1. Normalize
    query = normalize(statement)
    
    # 2. Retrieve
    faiss_hits = get_faiss_ranks(query, top_k=10)
    bm25_hits = get_bm25_ranks(query, top_k=10)
    
    # 3. Ensemble
    ensemble = EnsembleRetriever([faiss_hits, bm25_hits])
    top_verses = ensemble.retrieve(top_k=5)
    
    if not top_verses:
        return {
            "relevance": "NOT_RAMAYANA_RELATED",
            "label": "FALSE",
            "confidence_score": 0,
            "explanation": "No relevant verses found in the Ramayana database."
        }

    # 4. Verify
    verifier = ClaimVerifier(llm)
    result_json = verifier.verify_claim(statement, top_verses)
    
    # 5. Process References
    result_json = extract_ref(result_json, top_verses)
    
    return result_json
