from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import logging
from app.utils.learning_helpers import load_json_data, find_video_details, preprocess_ai_tools
GOOGLE_ID = os.getenv("GOOGLE_CLIENT_ID")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter()

# ============================================================
# ROBUST PATH CONFIG
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, "templates")


if not os.path.exists(TEMPLATE_DIR):
    logger.error(f"CRITICAL ERROR: Templates not found at {TEMPLATE_DIR}")
else:
    logger.info(f"SUCCESS: Templates loaded from {TEMPLATE_DIR}")

templates = Jinja2Templates(directory=TEMPLATE_DIR)

# ============================================================
# LOAD DATA SOURCES
# ============================================================
try:
    PYTHON_DATA = load_json_data('python_learning.json')
    ML_DATA = load_json_data('machine_learning.json')
    DL_DATA = load_json_data('deep_learning.json')
    ALGORITHMS_DATA = load_json_data('algorithms.json')
    SOFT_SKILLS_DATA = load_json_data('soft_skills.json')
    AI_TOOLS_RAW = load_json_data('ai_tools.json')
    AI_PROCESSED = preprocess_ai_tools(AI_TOOLS_RAW)
except Exception as e:
    logger.error(f"Error loading JSON data: {e}")
    PYTHON_DATA = ML_DATA = DL_DATA = ALGORITHMS_DATA = SOFT_SKILLS_DATA = []
    AI_PROCESSED = []


# ============================================================
# ROUTES
# ============================================================

# 1. Python Learning
@router.get("/python-learning/{video_id}", response_class=HTMLResponse)
async def python_learning(request: Request, video_id: str):
    current, topic, prev_v, next_v = find_video_details(video_id, PYTHON_DATA)
    if not current: raise HTTPException(status_code=404, detail="Video not found")
    return templates.TemplateResponse("course_python_learning.html", {
        "request": request,
        "google_client_id": GOOGLE_ID,
        "course_data": PYTHON_DATA, 
        "current_video": current, 
        "current_topic_name": topic, 
        "prev_video": prev_v, 
        "next_video": next_v
    })

# 2. Machine Learning
@router.get("/machine-learning/{video_id}", response_class=HTMLResponse)
async def machine_learning(request: Request, video_id: str):
    current, topic, prev_v, next_v = find_video_details(video_id, ML_DATA)
    if not current: raise HTTPException(status_code=404)
    return templates.TemplateResponse("course_machine_learning.html", {
        "request": request,
        "google_client_id": GOOGLE_ID,
        "course_data": ML_DATA, 
        "current_video": current, 
        "current_topic_name": topic, 
        "prev_video": prev_v, 
        "next_video": next_v
    })

# 3. Deep Learning
@router.get("/deep-learning-ai/{video_id}", response_class=HTMLResponse)
async def deep_learning_ai(request: Request, video_id: str):
    current, topic, prev_v, next_v = find_video_details(video_id, DL_DATA)
    if not current: raise HTTPException(status_code=404)
    return templates.TemplateResponse("course_data_learning.html", {
        "request": request,
        "google_client_id": GOOGLE_ID,
        "course_data": DL_DATA, 
        "current_video": current, 
        "current_topic_name": topic, 
        "prev_video": prev_v, 
        "next_video": next_v
    })

# 4. Algorithms
@router.get("/algorithms/{video_id}", response_class=HTMLResponse)
async def algorithms(request: Request, video_id: str):
    current, topic, prev_v, next_v = find_video_details(video_id, ALGORITHMS_DATA)
    if not current: raise HTTPException(status_code=404)
    return templates.TemplateResponse("course_algorithms.html", {
        "request": request,
        "google_client_id": GOOGLE_ID,
        "course_data": ALGORITHMS_DATA, 
        "current_video": current, 
        "current_topic_name": topic, 
        "prev_video": prev_v, 
        "next_video": next_v
    })

# 5. Soft Skills
@router.get("/soft-skills/{video_id}", response_class=HTMLResponse)
async def soft_skills(request: Request, video_id: str):
    current, topic, prev_v, next_v = find_video_details(video_id, SOFT_SKILLS_DATA)
    if not current: raise HTTPException(status_code=404)
    return templates.TemplateResponse("course_soft_skills.html", {
        "request": request,
        "google_client_id": GOOGLE_ID,
        "course_data": SOFT_SKILLS_DATA, 
        "current_video": current, 
        "current_topic_name": topic, 
        "prev_video": prev_v, 
        "next_video": next_v
    })

# 6. AI Tools
@router.get("/ai-tools/{tool_slug}", response_class=HTMLResponse)
async def ai_tools(request: Request, tool_slug: str):
    current_tool = None
    cat_name = None
    for cat in AI_PROCESSED:
        for t in cat['tools']:
            if t['slug'] == tool_slug:
                current_tool = t
                cat_name = cat['name']
                break
    return templates.TemplateResponse("course_ai_tools.html", {
        "request": request,
        "google_client_id": GOOGLE_ID,
        "ai_tools_data": AI_PROCESSED, 
        "current_tool": current_tool, 
        "current_category_name": cat_name
    })

# 7. English Learning Hub
@router.get("/english-learning", response_class=HTMLResponse, name="english_learning")
async def english_learning(request: Request):
    return templates.TemplateResponse("english_learning_hub.html", {"request": request})
