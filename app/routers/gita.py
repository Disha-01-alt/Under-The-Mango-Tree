import os
import json
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Path Config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, "templates")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
STATIC_DIR = os.path.join(PROJECT_ROOT, "static")

templates = Jinja2Templates(directory=TEMPLATE_DIR)

@router.get("/gita-portal", response_class=HTMLResponse)
async def gita_portal(request: Request):
    return templates.TemplateResponse("gita_portal.html", {"request": request})

@router.get("/api/gita-data")
async def get_gita_data():
    json_path = os.path.join(DATA_DIR, "updated_file.json")
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as e:
        return JSONResponse(status_code=404, content={"error": "Gita data not found"})

@router.get("/api/check-pdf")
async def check_pdf(path: str):
    filename = os.path.basename(path)
    # Correct path to your PDF storage
    pdf_path = os.path.join(STATIC_DIR, "gita_portal_data", "pdfs", filename)
    exists = os.path.exists(pdf_path)
    return {"exists": exists, "path": f"/static/gita_portal_data/pdfs/{filename}" if exists else None}
