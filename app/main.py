from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(title="DevOps Learning App")

# Mount static files (if we had any, but good practice to have setup)
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Include Routers
from routers import bible, terraform
app.include_router(bible.router)
app.include_router(terraform.router)

from routers.bible import CHAPTERS

@app.get("/god_mode", response_class=HTMLResponse)
async def god_mode(request: Request):
    return templates.TemplateResponse("god_mode.html", {"request": request})

@app.get("/arena", response_class=HTMLResponse)
async def arena(request: Request):
    """Global Knowledge Arena — aggregates all quiz questions across chapters."""
    pool = []
    for ch in CHAPTERS:
        for q in ch.get("quiz", []):
            pool.append({
                "q": q["q"],
                "options": q["options"],
                "a": q["a"],
                "source_title": ch["title"],
                "source_id": ch["id"],
            })
    return templates.TemplateResponse("global_test.html", {
        "request": request,
        "questions": pool,
        "total": len(pool),
    })

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "chapters": CHAPTERS
    })

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
