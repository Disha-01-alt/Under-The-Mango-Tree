# app/inference/response_gen.py

import json
import re
from dotenv import load_dotenv
from app.llm_providers.api_client import get_llm_client

load_dotenv()
llm = get_llm_client()


# --------------------------------------------------
# CLEAN LLM JSON OUTPUT
# --------------------------------------------------
def clean_llm_json(text: str) -> dict:
    """
    Handles DeepSeek 'think' tags and ensures a clean JSON object 
    with expected keys is returned.
    """
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

    try:
        match = re.search(r'(\{.*\})', text, re.DOTALL)
        if not match:
            return {
                "summary_answer": "Neural Synthesis",
                "detailed_answer": text,
                "references": []
            }

        data = json.loads(match.group(1))
        return {
            "summary_answer": data.get("summary_answer", "Neural Synthesis"),
            "detailed_answer": data.get("detailed_answer", ""),
            "references": data.get("references", [])
        }

    except Exception:
        return {
            "summary_answer": "Neural Synthesis",
            "detailed_answer": text,
            "references": []
        }


# --------------------------------------------------
# MAIN RESPONSE FUNCTION
# --------------------------------------------------
def get_bot_response(question: str, row: dict | None) -> dict:
    """
    row contains authoritative DB fields:
    chapter, verse, speaker, sanskrit, translation, youtube_link, download_link
    """

    # -------------------------------
    # CASE 1: DB MISS
    # -------------------------------
    if not row:
        system_prompt = (
            "You are a spiritual teacher.\n"
            "No specific scripture record was found for this query.\n"
            "Provide a general spiritual explanation based on Vedic wisdom.\n"
            "Do NOT fabricate verse numbers or chapter titles.\n"
            "Return ONLY valid JSON:\n"
            "{\"summary_answer\": \"...\", \"detailed_answer\": \"...\", \"references\": []}"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Question: {question}"}
        ]

        raw = llm.generate(messages=messages, max_tokens=800)
        return clean_llm_json(raw)

    # -------------------------------
    # CASE 2: DB HIT (STRICT COMMENTARY)
    # -------------------------------
    system_prompt = (
        "You are a spiritual commentator.\n\n"
        "You are provided with a VERIFIED scripture record from the database.\n"
        "Explain the meaning of this specific verse in relation to the user's question.\n\n"
        "STRICT RULES:\n"
        "- Do NOT modify the provided Chapter, Verse, or Sanskrit text.\n"
        "- Do NOT include the Sanskrit or Translation strings in your 'detailed_answer' (they are shown separately).\n"
        "- ONLY provide summary and philosophical explanation.\n"
        "- Keep the 'detailed_answer' under 200 words.\n\n"
        "Return ONLY valid JSON:\n"
        "{\"summary_answer\": \"...\", \"detailed_answer\": \"...\", \"references\": []}"
    )

    user_prompt = (
        f"Question: {question}\n\n"
        f"Scripture Record:\n"
        f"Speaker: {row.get('speaker', 'Unknown')}\n"
        f"Chapter: {row['chapter']}\n"
        f"Verse: {row['verse']}\n"
        f"Sanskrit: {row['sanskrit']}\n"
        f"Translation: {row['translation']}\n"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    raw = llm.generate(messages=messages, max_tokens=1200)
    response = clean_llm_json(raw)

    # --------------------------------------------------
    # 🔗 ATTACH AUTHORITATIVE LINKS & REFERENCES
    # --------------------------------------------------
    # We pull these directly from the DB 'row', NOT the LLM.
    yt_link = row.get('youtube_link')
    dl_link = row.get('download_link')

    # Top-level keys (Important for Cache logic)
    response["youtube_link"] = yt_link
    response["download_link"] = dl_link

    # Reference structure
    response["references"] = [
        {
            "chapter": row["chapter"],
            "verse": row["verse"],
            "speaker": row.get("speaker"),
            "sanskrit": row["sanskrit"],
            "translation": row["translation"],
            "youtube_link": yt_link,
            "download_link": dl_link,
            "metadata": row.get("metadata", {})
        }
    ]

    return response
