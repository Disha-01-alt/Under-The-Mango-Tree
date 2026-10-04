# Under The Mango Tree (UTMT)

A unified FastAPI platform (`Sanatana AI Backend`) that serves both the frontend UI and the AI backend on a single port. It combines:

- **Learning Hub** — course content and user history (`app/routers/learning.py`)
- **Sacred Oracle (Gita portal)** — a pgvector RAG pipeline over scripture (`app/routers/gita.py`, `app/inference/`)
- **IYD** — claim / truth verification over the Ramayana (`app/IYD/`)
- **Provider-agnostic LLM client** — any OpenAI-compatible chat + embedding provider (`app/llm_providers/`)

## 1. Project Structure

```
utmt/
├── main.py                  <-- Main FastAPI application entry (app = FastAPI(...))
├── .env                     <-- Configuration (not committed)
├── requirements.txt         <-- Dependencies
├── app/                     <-- Core logic modules
│   ├── db/                  <-- Database logic (init_pgvector.py, pg_vector_store.py)
│   ├── dataset/             <-- Raw CSVs & conversion scripts
│   ├── IYD/                 <-- Ramayana truth-verification module
│   ├── inference/           <-- RAG pipeline (retrieval, filtering, generation)
│   ├── llm_providers/       <-- Generic OpenAI-compatible LLM/embedding client
│   ├── routers/             <-- Route modules (learning.py, gita.py)
│   ├── scripts/             <-- Data ingestion scripts
│   └── utils/               <-- Query filters and helpers
├── static/                  <-- Assets (CSS, JS, images)
├── data/                    <-- JSON datasets (learning.json, projects.json, …)
└── templates/               <-- HTML templates (index, courses, gita_portal, …)
```

## 2. Environment Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root (provider-agnostic keys):

```bash
# ===== GOOGLE AUTHENTICATION =====
GOOGLE_CLIENT_ID=your_google_client_id.apps.googleusercontent.com

# ===== LLM (Generation - any OpenAI-compatible provider) =====
LLM_PROVIDER=openai
CHAT_API_KEY=your_api_key_here
CHAT_MODEL=llama-3.3-70b-versatile
CHAT_BASE_URL=https://api.groq.com/openai/v1   # swap for OpenAI, Together, DeepSeek, …

# ===== Embeddings (RAG) =====
EMBEDDING_PROVIDER=mistral
EMBEDDING_API_KEY=your_mistral_key_here
EMBEDDING_MODEL=mistral-embed
EMBEDDING_API_URL=https://api.mistral.ai/v1/embeddings

# ===== PostgreSQL (pgvector) =====
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=iks_rag
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password

# ===== Deployment =====
ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

> `.env` is git-ignored — never commit real keys.

| `CHAT_MODEL` | Provider |
|---|---|
| `llama-3.3-70b-versatile` | Groq |
| `deepseek-r1-distill-llama-70b` | Groq / DeepSeek |
| `gpt-4o` / `gpt-4o-mini` | OpenAI |
| `mistral-large-latest` | Mistral |

## 3. Database Initialization

**Step A — create tables** (sets up vector dimensions and link columns):

```bash
export PYTHONPATH=$PYTHONPATH:.
python3 app/db/init_pgvector.py
```

**Step B — ingest scripture data.** Place `gita_collection.csv` and `yoga_collection.csv` in `app/dataset/` with headers: `chapter, verse, speaker, sanskrit, translation, youtube_link, download_link`.

```bash
python3 app/scripts/ingest_test_data.py
```

## 4. Running the Platform

FastAPI serves both the frontend and the AI backend on the same port — do **not** use Live Server.

```bash
uvicorn main:app --reload --port 8000
```

Then open <http://localhost:8000>.
