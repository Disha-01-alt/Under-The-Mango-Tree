import os
import psycopg2
from dotenv import load_dotenv
from app.llm_providers.api_client import get_llm_client

load_dotenv()

def init_pgvector():
    # 1️⃣ Detect embedding dimension dynamically
    print("🔍 Detecting embedding dimensions...")
    llm = get_llm_client()
    test_embedding = llm.embed("Namaste")
    dim = len(test_embedding)
    print(f"✅ Embedding dimension detected: {dim}")

    # 2️⃣ Connect to Postgres
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=int(os.getenv("POSTGRES_PORT", 5432)),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
    conn.autocommit = True
    cur = conn.cursor()

    # 3️⃣ Enable pgvector and check version for halfvec support
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    cur.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector';")
    version = cur.fetchone()[0]
    print(f"📦 pgvector version: {version}")

    # 4️⃣ DROP existing tables
    print("⚠️ Dropping existing tables...")
    cur.execute("DROP TABLE IF EXISTS qna_collection CASCADE;")
    cur.execute("DROP TABLE IF EXISTS gita_collection CASCADE;")
    cur.execute("DROP TABLE IF EXISTS yoga_collection CASCADE;")
    cur.execute("DROP TABLE IF EXISTS ramayana_collection CASCADE;")

    # 5️⃣ Create Knowledge Tables
    print("📘 Creating Gita, Yoga & Ramayana collections...")
    for table in ["gita_collection", "yoga_collection", "ramayana_collection"]:
        cur.execute(f"""
            CREATE TABLE {table} (
                id SERIAL PRIMARY KEY,
                embedding VECTOR({dim}),
                chapter TEXT,
                verse TEXT,
                speaker TEXT,
                sanskrit TEXT,
                translation TEXT,
                youtube_link TEXT,
                download_link TEXT,
                metadata JSONB
            );
        """)
        
        # ✅ DYNAMIC CAST: Use the detected 'dim' variable
        if dim > 2000:
            print(f"   ↳ Creating HNSW index on halfvec for {table} (Dim: {dim})...")
            cur.execute(f"""
                CREATE INDEX ON {table} 
                USING hnsw ((embedding::halfvec({dim})) halfvec_cosine_ops);
            """)
        else:
            print(f"   ↳ Creating standard HNSW index for {table}...")
            cur.execute(f"CREATE INDEX ON {table} USING hnsw (embedding vector_cosine_ops);")

    # 6️⃣ Create QnA Cache Table
    print("🧠 Creating QnA cache table...")
    cur.execute(f"""
        CREATE TABLE qna_collection (
            id SERIAL PRIMARY KEY,
            embedding VECTOR({dim}),
            question_text TEXT,
            normalized_question TEXT NOT NULL,
            summary_answer TEXT,
            detailed_answer TEXT,
            youtube_link TEXT,
            download_link TEXT,
            mode TEXT NOT NULL,
            user_id TEXT,
            session_id TEXT,
            metadata JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    if dim > 2000:
        print(f"   ↳ Creating HNSW index on halfvec for qna_collection (Dim: {dim})...")
        cur.execute(f"""
            CREATE INDEX ON qna_collection 
            USING hnsw ((embedding::halfvec({dim})) halfvec_cosine_ops);
        """)
    else:
        cur.execute("CREATE INDEX ON qna_collection USING hnsw (embedding vector_cosine_ops);")

    cur.execute("CREATE INDEX idx_qna_normalized_q ON qna_collection(normalized_question);")

    # UNIQUE INDEX for deduplication
    cur.execute("""
        CREATE UNIQUE INDEX uq_qna_user_scope 
        ON qna_collection(mode, normalized_question, COALESCE(user_id, ''), COALESCE(session_id, ''));
    """)

    cur.close()
    conn.close()
    print("🚀 Database initialized successfully!")

if __name__ == "__main__":
    init_pgvector()
