1. Unified Project Structure
utmt/
├── app.py                   <-- Main FastAPI Application Entry
├── .env                     <-- Generic Global Configuration
├── requirements.txt         <-- Unified Dependencies
├── app/                     <-- Core Logic Modules
│   ├── db/                  <-- Database logic (init_pgvector.py, pg_vector_store.py)
│   ├── dataset/             <-- Raw CSVs & ingest_script.py
│   ├── iyd/                 <-- Truth Verification (IYD) Module
│   ├── inference/           <-- Sacred Oracle (NYD) RAG Pipeline
│   ├── llm_providers/       <-- Generic LLM API Client (OpenAI-compatible)
│   ├── routers/             <-- Hub Routing (learning.py)
│   └── utils/               <-- Query filters and helpers
├── static/                  <-- Assets (CSS, JS, Images, Logo)
├── data/                    <-- JSON datasets (learning.json, projects.json)
└── templates/               <-- HTML Templates (index, user_history, courses)

2. Environment Setup
Install Dependencies
Activate your environment and install the unified requirement list:
pip install -r requirements.txt
Configure the .env File
Create a .env file in the root utmt/ directory. Use generic keys to ensure the project remains provider-agnostic:
# ===== GOOGLE AUTHENTICATION =====
GOOGLE_CLIENT_ID=292573049990-t8arlb44ossvelf81j9tvlgdev8c4ee0.apps.googleusercontent.com

# ===== LLM (Generation - Any OpenAI-compatible Provider) =====
LLM_PROVIDER=openai
CHAT_API_KEY=your_api_key_here
CHAT_MODEL=llama-3.3-70b-versatile
CHAT_BASE_URL=https://api.groq.com/openai/v1  # Change this to use OpenAI, Together, or DeepSeek

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
Permissible Models for CHAT_MODEL	Provider
llama-3.3-70b-versatile	Groq
deepseek-r1-distill-llama-70b	Groq / DeepSeek
gpt-4o / gpt-4o-mini	OpenAI
mistral-large-latest	Mistral

3. Database Initialization
Step A: Create Tables
Run the initialization script from the root directory to set up tables with correct vector dimensions and link columns.
export PYTHONPATH=$PYTHONPATH:.
python3 app/db/init_pgvector.py
Step B: Ingest Scripture Data
Ensure your gita_collection.csv and yoga_collection.csv are in app/dataset/ with headers: chapter, verse, speaker, sanskrit, translation, youtube_link, download_link.
python3 app/scripts/ingest_test_data.py

4. Running the Platform
In this unified structure, FastAPI serves both the high-end Frontend and the AI Backend on the same port. Do not use Live Server.
Start the server:
uvicorn app:app --reload --port 8000
Access the UI:
Open http://localhost:8000
