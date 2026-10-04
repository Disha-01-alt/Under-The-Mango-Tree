import os
import sys
import logging
import requests
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# ============================================================
# PATH CONFIG (Robust for Deployment)
# ============================================================

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Add root to sys.path for internal app imports
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

STATIC_DIR = os.path.join(ROOT_DIR, "static")
DATA_DIR = os.path.join(ROOT_DIR, "data")
TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")
# ============================================================
# IMPORTS
# ============================================================

from app.routers import learning
from app.routers import gita
from app.inference.pipeline import pipeline_rag_cache
from app.inference.retrieve_cache import retrieve_context_cache
from app.db.pg_vector_store import PGVectorStore
vector_store = PGVectorStore()
from app.IYD.service import verify_claim_service

# ============================================================
# GOOGLE AUTH CONFIG
# ============================================================
GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")  # REQUIRED
# ============================================================
# APP SETUP & CORS (Updated for Production)
# ============================================================
app = FastAPI(title="Sanatana AI Backend")

raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000,http://localhost:5500")
origins = [origin.strip() for origin in raw_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/data", StaticFiles(directory=DATA_DIR), name="data")

# Initialize Jinja2 for HTML rendering
templates = Jinja2Templates(directory=TEMPLATES_DIR)

app.include_router(learning.router)
app.include_router(gita.router)

# ============================================================
# GOOGLE AUTH DEPENDENCY (STRICT)
# ============================================================
def require_google_user(request: Request) -> dict:
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        logger.error("Authorization header missing or ill-formatted")
        raise HTTPException(status_code=401, detail="Authentication required")

    token = auth_header.replace("Bearer ", "").strip()
    
    if not token or token in ["null", "undefined", ""]:
        logger.error("Invalid token string received")
        raise HTTPException(status_code=401, detail="Invalid session")

    # Validate with Google
    resp = requests.get(GOOGLE_TOKEN_INFO_URL, params={"id_token": token})
    if resp.status_code != 200:
        logger.error(f"Google Token Validation Failed: {resp.text}")
        raise HTTPException(status_code=401, detail="Session expired. Please log in again.")

    payload = resp.json()

    if payload.get("aud") != GOOGLE_CLIENT_ID:
        logger.error(f"Audience mismatch: {payload.get('aud')}")
        raise HTTPException(status_code=401, detail="Invalid token source")

    # FIXED: Define is_verified from the payload before checking it
    is_verified = payload.get("email_verified")
    
    if is_verified not in [True, "true"]:
        logger.warning(f"User {payload.get('email')} has an unverified email.")

    # Final Return (Ensuring it is a dict with 'user_id')
    return {
        "user_id": payload["sub"],
        "email": payload.get("email"),
        "name": payload.get("name"),
    }
# ============================================================
# MODELS
# ============================================================
class ChatRequest(BaseModel):
    query: str


class VerifyRequest(BaseModel):
    statement: str

# ============================================================
# NYD CHAT (AUTH REQUIRED)
# ============================================================
@app.post("/v1/chat/nyd")
async def chat_nyd(
    payload: ChatRequest,
    user=Depends(require_google_user),
):
    if not payload.query or len(payload.query.strip()) < 2:
        return JSONResponse(
            content={
                "summary_answer": "Invalid Query",
                "detailed_answer": "Please ask a meaningful question.",
                "references": [],
            }
        )

    mode = "NYD"
    user_id = user["user_id"]

    # 1️⃣ CACHE (USER → GLOBAL)
    cached = retrieve_context_cache(
        query=payload.query,
        mode=mode,
        user_id=user_id,
    )
    if cached:
        return JSONResponse(content=jsonable_encoder(cached))

    # 2️⃣ PIPELINE
    try:
        result = pipeline_rag_cache(
            query=payload.query,
            mode=mode,
            user_id=user_id,
        )
        return JSONResponse(content=jsonable_encoder(result))

    except Exception:
        logger.exception("NYD failed")
        return JSONResponse(
            status_code=500,
            content={
                "summary_answer": "System Error",
                "detailed_answer": "Internal error occurred",
                "references": [],
            },
        )

# ============================================================
# IYD VERIFY (AUTH REQUIRED)
# ============================================================
@app.post("/v1/iyd/verify")
async def verify_iyd(
    payload: VerifyRequest,
    user=Depends(require_google_user),
):
    if not verify_claim_service:
        raise HTTPException(status_code=503, detail="IYD unavailable")

    mode = "IYD"
    user_id = user["user_id"]

    # 1️⃣ CACHE
    cached = retrieve_context_cache(
        query=payload.statement,
        mode=mode,
        user_id=user_id,
    )
    if cached:
        return JSONResponse(content=jsonable_encoder(cached))

    try:
        # Pass the user_id as the second argument
        result = verify_claim_service(payload.statement, user_id) 
        return JSONResponse(content=jsonable_encoder(result))

    except Exception:
        logger.exception("IYD failed")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal verification error"},
        )


@app.get("/user-history")
async def user_history_page(request: Request):
    return templates.TemplateResponse("user_history.html", {
        "request": request,
        "google_client_id": GOOGLE_CLIENT_ID  
    })

@app.get("/v1/user/history")
async def get_user_history(user=Depends(require_google_user)):
    user_id = user["user_id"]
    try:
        with vector_store.conn.cursor() as cur:
            cur.execute("""
                SELECT question_text, summary_answer, detailed_answer, created_at, mode, 
                       youtube_link, download_link, metadata
                FROM qna_collection
                WHERE user_id = %s
                ORDER BY created_at DESC;
            """, (user_id,))
            rows = cur.fetchall()
        
        history = []
        for r in rows:
            raw_meta = r[7] # metadata is now index 7
            if isinstance(raw_meta, (list, dict)): meta_list = raw_meta
            elif isinstance(raw_meta, str): meta_list = json.loads(raw_meta)
            else: meta_list = []
            
            history.append({
                "question": r[0],
                "summary": r[1],  # Added summary_answer (The Verdict)
                "answer": r[2],   # detailed_answer
                "date": r[3].strftime("%Y-%m-%d %H:%M"),
                "category": r[4],
                "youtube_link": r[5],
                "download_link": r[6],
                "references": meta_list 
            })
        return JSONResponse(content={"history": history})
    except Exception as e:
        logger.error(f"History Fetch Error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": "Process failed"})
# ============================================================
# HEALTH
# ============================================================
@app.get("/status")
def status():
    return {
        "status": "online",
        "timestamp": datetime.utcnow().isoformat(),
        "auth": "google-only",
        "services": {
            "nyd": "ready",
            "iyd": "ready" if verify_claim_service else "offline",
            "learning": "ready"
        },
    }
@app.get("/", name="home") 
async def home(request: Request): 
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "google_client_id": GOOGLE_CLIENT_ID  
    })

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    # This allows the Google Login popup to talk back to your window
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin-allow-popups"
    return response
