import os
import json
import psycopg2
import logging
from psycopg2.extras import execute_values
from app.llm_providers.api_client import get_llm_client

logger = logging.getLogger(__name__)

def normalize_question(q: str) -> str:
    return (
        q.lower()
        .strip()
        .replace("?", "")
        .replace(".", "")
        .replace(",", "")
    )

class PGVectorStore:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
        
        # 1. Detect Dimension from the configured LLM provider
        self.dim = self._detect_dimension()
        logger.info(f"🚀 PGVectorStore initialized with dimension: {self.dim}")
        
        # 2. Initialize tables with the correct dimension
        self._initialize_tables()

    def _detect_dimension(self):
        """Detects embedding dimension by calling the provider once."""
        try:
            llm = get_llm_client()
            test_emb = llm.embed("dimension_check")
            return len(test_emb)
        except Exception as e:
            logger.error(f"Failed to detect embedding dimension: {e}")
            # Fallback based on provider name if API call fails
            provider = os.getenv("EMBEDDING_PROVIDER", "gemini").lower()
            if provider == "gemini": return 768
            if provider == "mistral": return 1024
            return 1536 # Default for OpenAI

    def _initialize_tables(self):
        with self.conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

            # Knowledge Tables
            for table in ["gita_collection", "yoga_collection", "ramayana_collection"]:
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {table} (
                        id SERIAL PRIMARY KEY,
                        embedding vector({self.dim}),
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

            # QnA Cache Table
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS qna_collection (
                    id SERIAL PRIMARY KEY,
                    embedding vector({self.dim}),
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

            cur.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS uq_qna_user_scope
                ON qna_collection(mode, normalized_question, COALESCE(user_id, ''), COALESCE(session_id, ''));
            """)
            self.conn.commit()

    def upsert_knowledge(self, table, records):
        with self.conn.cursor() as cur:
            execute_values(
                cur,
                f"INSERT INTO {table} (embedding, chapter, verse, speaker, sanskrit, translation, youtube_link, download_link, metadata) VALUES %s;",
                records,
            )
            self.conn.commit()

    def get_exact_cache(self, question, mode, user_id=None):
        normalized = normalize_question(question)
        with self.conn.cursor() as cur:
            sql = "SELECT * FROM qna_collection WHERE normalized_question = %s AND mode = %s"
            params = [normalized, mode]
            
            if user_id:
                sql += " AND user_id = %s"
                params.append(user_id)
            else:
                sql += " AND user_id IS NULL"
            
            cur.execute(sql + " LIMIT 1;", params)
            rows = self._format(cur, cur.fetchall())
            return rows[0] if rows else None

    def search_qna_cache(self, embedding, mode, user_id=None, top_k=1):
        # REMOVED hardcoded [:1024] slice
        with self.conn.cursor() as cur:
            if user_id:
                cur.execute("""
                    SELECT *, (embedding <=> %s::vector) AS distance
                    FROM qna_collection
                    WHERE mode=%s AND user_id=%s
                    ORDER BY distance ASC LIMIT %s;
                """, (embedding, mode, user_id, top_k))
            else:
                cur.execute("""
                    SELECT *, (embedding <=> %s::vector) AS distance
                    FROM qna_collection
                    WHERE mode=%s AND user_id IS NULL
                    ORDER BY distance ASC LIMIT %s;
                """, (embedding, mode, top_k))
            return self._format(cur, cur.fetchall())

    def insert_qna_cache(
        self, embedding, question, summary, detailed, 
        youtube_link, download_link, mode, metadata, user_id=None, session_id=None
    ):
        # REMOVED hardcoded [:1024] slice
        normalized = normalize_question(question)
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO qna_collection
                (embedding, question_text, normalized_question, summary_answer, 
                 detailed_answer, youtube_link, download_link, mode, user_id, session_id, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (mode, normalized_question, COALESCE(user_id, ''), COALESCE(session_id, '')) 
                DO UPDATE SET 
                    embedding = EXCLUDED.embedding,
                    summary_answer = EXCLUDED.summary_answer,
                    detailed_answer = EXCLUDED.detailed_answer;
            """, (
                embedding, question, normalized, summary, 
                detailed, youtube_link, download_link, mode, user_id, session_id, json.dumps(metadata)
            ))
            self.conn.commit()

    def search_knowledge(self, embedding, table, top_k=5):
        # REMOVED hardcoded [:1024] slice
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT *, (embedding <=> %s::vector) AS distance FROM {table} ORDER BY distance ASC LIMIT %s;", (embedding, top_k))
            return self._format(cur, cur.fetchall())

    def _format(self, cur, rows):
        if not rows: return []
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in rows]

    def question_exists(self, mode, normalized_question, user_id=None):
        normalized_question = normalize_question(normalized_question)
        with self.conn.cursor() as cur:
            if user_id:
                cur.execute("SELECT 1 FROM qna_collection WHERE mode=%s AND normalized_question=%s AND user_id=%s LIMIT 1;", (mode, normalized_question, user_id))
            else:
                cur.execute("SELECT 1 FROM qna_collection WHERE mode=%s AND normalized_question=%s AND user_id IS NULL LIMIT 1;", (mode, normalized_question))
            return cur.fetchone() is not None
