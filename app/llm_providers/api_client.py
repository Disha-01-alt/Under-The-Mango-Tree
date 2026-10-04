import os
import re
import json
import time
import random
import requests
import logging
import google.generativeai as genai
from dotenv import load_dotenv
import openai

load_dotenv()
logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        # 1. Generation Configuration
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.api_key = os.getenv("CHAT_API_KEY")
        self.model = os.getenv("CHAT_MODEL", "gemini-1.5-flash")
        self.base_url = os.getenv("CHAT_BASE_URL")

        # 2. Embedding Configuration
        self.embed_provider = os.getenv("EMBEDDING_PROVIDER", "openai").lower()
        self.embed_api_key = os.getenv("EMBEDDING_API_KEY")
        self.embed_model = os.getenv("EMBEDDING_MODEL", "models/text-embedding-004")
        self.embed_url = os.getenv("EMBEDDING_API_URL")

        # 3. Initialize Chat Client
        if self.provider == "gemini":
            genai.configure(api_key=self.api_key)
        elif self.provider != "dummy":
            self.openai_client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)

    def generate(self, messages, temperature=0.2, max_tokens=1024, max_retries=3):
        """Standardized generation with retry logic for Free Tier stability."""
        if self.provider == "dummy":
            return self._dummy_response()

        for attempt in range(max_retries):
            try:
                if self.provider == "gemini":
                    return self._generate_gemini_sdk(messages, temperature, max_tokens)
                
                # OpenAI / Groq Branch
                response = self.openai_client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                content = response.choices[0].message.content
                return re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()

            except Exception as e:
                err_msg = str(e).lower()
                # Handle Rate Limits (429) or Service Overloaded (503/504)
                if "429" in err_msg or "quota" in err_msg or "exhausted" in err_msg or "503" in err_msg:
                    wait_time = (2 ** attempt) + random.random()
                    logger.warning(f"Chat API rate limited. Retry {attempt+1}/{max_retries} in {wait_time:.2f}s...")
                    time.sleep(wait_time)
                    continue
                
                # Handle Gemini 404 Fallback
                if self.provider == "gemini" and ("404" in err_msg or "not found" in err_msg):
                    logger.warning("Gemini SDK 404. Trying REST fallback...")
                    return self._generate_gemini_rest(messages, temperature, max_tokens)

                logger.error(f"LLM Generation Error: {e}")
                break
        
        return "The oracle is momentarily silent. (Rate limit or API error)"

    def _generate_gemini_sdk(self, messages, temperature, max_tokens):
        model_name = self.model.replace("models/", "")
        sys_msg = next((m['content'] for m in messages if m['role'] == 'system'), None)
        
        model = genai.GenerativeModel(model_name=model_name, system_instruction=sys_msg)
        history = []
        for m in messages:
            if m['role'] == 'system': continue
            role = "user" if m['role'] == 'user' else "model"
            history.append({"role": role, "parts": [{"text": m['content']}]})

        user_prompt = history.pop()["parts"][0]["text"]
        chat = model.start_chat(history=history)
        response = chat.send_message(
            user_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature, max_output_tokens=max_tokens
            )
        )
        return response.text

    def _generate_gemini_rest(self, messages, temperature, max_tokens):
        try:
            model_name = self.model.replace("models/", "")
            url = f"https://generativelanguage.googleapis.com/v1/models/{model_name}:generateContent?key={self.api_key}"
            contents = []
            system_instruction = None
            for m in messages:
                if m['role'] == 'system':
                    system_instruction = {"parts": [{"text": m['content']}]}
                else:
                    role = "user" if m['role'] == 'user' else "model"
                    contents.append({"role": role, "parts": [{"text": m['content']}]})

            payload = {"contents": contents, "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens}}
            if system_instruction: payload["systemInstruction"] = system_instruction

            resp = requests.post(url, json=payload, timeout=30)
            resp.raise_for_status()
            return resp.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            logger.error(f"Gemini REST Error: {e}")
            return "The Gemini REST Oracle is silent."

    def embed(self, text: str, max_retries=3):
        """Embedding method with Exponential Backoff and Zero-Vector protection."""
        if not text or not text.strip():
            return [0.0] * (768 if self.embed_provider == "gemini" else 1024)

        for attempt in range(max_retries):
            try:
                if self.embed_provider == "gemini":
                    m = self.embed_model if self.embed_model.startswith("models/") else f"models/{self.embed_model}"
                    result = genai.embed_content(model=m, content=text, task_type="retrieval_document")
                    embedding = result['embedding']
                    
                    # VALIDATION: Check for all-zero vectors (prevents NaN errors)
                    if sum(map(abs, embedding)) == 0:
                        raise ValueError("Received an all-zero embedding vector.")
                    return embedding

                # OpenAI / Mistral Branch
                headers = {"Authorization": f"Bearer {self.embed_api_key}", "Content-Type": "application/json"}
                payload = {"model": self.embed_model, "input": [text]}
                response = requests.post(self.embed_url, json=payload, headers=headers, timeout=60)
                response.raise_for_status()
                return response.json()["data"][0]["embedding"]

            except Exception as e:
                err_msg = str(e).lower()
                if "429" in err_msg or "quota" in err_msg or "exhausted" in err_msg or "503" in err_msg:
                    wait_time = (2 ** attempt) + random.random()
                    logger.warning(f"Embedding rate limited. Retry {attempt+1}/{max_retries} in {wait_time:.2f}s...")
                    time.sleep(wait_time)
                    continue
                
                logger.error(f"Embedding API Error: {e}")
                break

        # Return a zero vector if all retries fail (prevents total crash)
        return [0.0] * (768 if self.embed_provider == "gemini" else 1024)

    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        return self.generate([{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}])

    def _dummy_response(self):
        return json.dumps({"label": "TRUE", "explanation": "Dummy response."})

def get_llm_client():
    return LLMClient()
