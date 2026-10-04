import re
import os
from better_profanity import profanity
from dotenv import load_dotenv
from app.llm_providers.api_client import get_llm_client

load_dotenv()
llm = get_llm_client()
profanity.load_censor_words()

# --------------------------------------------------
# NORMALIZATION
# --------------------------------------------------
def normalize_text(text: str) -> str:
    return text.lower().strip()

# --------------------------------------------------
# OFFENSIVE / GIBBERISH FILTER (1=INVALID, 0=VALID)
# --------------------------------------------------
def check_offensive_language(text: str) -> int:
    """
    Returns 1 for Gibberish, Symbols, or Profanity.
    Returns 0 for meaningful text.
    """
    if not text: return 1
    
    # Clean text for symbol check
    text_clean = re.sub(r'[^\w\s]', '', text.lower()).strip()
    
    # 1. Block Pure Symbols or repeated gibberish (&&, ???, vvvv)
    if not text_clean or re.match(r'^(.)\1{2,}$', text_clean):
        return 1
        
    # 2. Block short non-spiritual fragments (ver, veri, asd)
    valid_short = {'om', 'yoga', 'gita', 'atma', 'god'}
    if len(text_clean) < 4 and text_clean not in valid_short:
        return 1

    # 3. Block malformed triggers specifically
    if re.search(r'veri\+|&&', text.lower()):
        return 1

    # 4. Profanity filter
    if profanity.contains_profanity(text):
        return 1

    return 0

# --------------------------------------------------
# RELEVANCE GATEKEEPER (1=IRRELEVANT, 0=RELEVANT)
# --------------------------------------------------
def check_valid(query: str) -> int:
    """
    Hard Gate: Rejects modern junk using the LLM provider.
    Standardized: Returns 1 if Irrelevant, 0 if Relevant.
    """
    # Priority bypass: If they mention these words, they are definitely relevant (Return 0)
    priority_words = ['gita', 'yoga', 'karma', 'dharma', 'krishna', 'sutra', 'atman', 'god', 'peace']
    if any(w in query.lower() for w in priority_words):
        return 0

    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an advanced text classifier for a Vedic Wisdom chatbot.\n\n"
                    "Strictly classify the input as either:\n"
                    "1️⃣ **Output '1' (Irrelevant)** if the sentence is unrelated to spiritual wisdom. This includes:\n"
                    "   - Modern politics, sports, celebrity news, pop culture, or tech support.\n"
                    "   - Generic chit-chat like 'How is the weather?' or 'Who is the president?'.\n\n"
                    "2️⃣ **Output '0' (Relevant)** if the sentence is a spiritual or philosophical inquiry. This includes:\n"
                    "   - Questions about enlightenment, dharma, karma, soul, or meditation.\n"
                    "   - Requests for philosophical life advice.\n\n"
                    "⚠️ **Strictly follow the format:** Your response must be either '1' or '0' with no other text."
                ),
            },
            {"role": "user", "content": f"Query: {query}"}
        ]
        
        response = llm.generate(messages=messages, max_tokens=5, temperature=0)
        
        # If the LLM output contains '1', it is irrelevant
        if "1" in response:
            return 1
        return 0
        
    except Exception as e:
        print(f"Filter Error: {e}")
        # Fallback: On error, allow the question to pass to the RAG pipeline (Return 0)
        return 0
