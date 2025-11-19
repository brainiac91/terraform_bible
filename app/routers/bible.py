from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import markdown
import os

router = APIRouter(
    prefix="/bible",
    tags=["bible"]
)

templates = Jinja2Templates(directory="templates")
CHAPTERS_DIR = "content/chapters"

CHAPTERS = [
    {"id": "01_intro", "title": "1. Introduction & Setup"},
    {"id": "02_workflow", "title": "2. The Terraform Workflow"},
    {"id": "03_state", "title": "3. Mastering State"},
    {"id": "04_variables_outputs", "title": "4. Variables & Outputs"},
    {"id": "05_modules", "title": "5. Module Architecture"},
    {"id": "06_advanced_hcl", "title": "6. Advanced HCL Patterns"},
    {"id": "07_testing_validation", "title": "7. Testing & Validation"},
    {"id": "08_production", "title": "8. Production Best Practices"},
]

@router.get("/{chapter_id}", response_class=HTMLResponse)
async def get_chapter(request: Request, chapter_id: str):
    # Find current chapter index
    try:
        current_index = next(i for i, c in enumerate(CHAPTERS) if c["id"] == chapter_id)
    except StopIteration:
        raise HTTPException(status_code=404, detail="Chapter not found")

    # Navigation logic
    prev_chapter = CHAPTERS[current_index - 1] if current_index > 0 else None
    next_chapter = CHAPTERS[current_index + 1] if current_index < len(CHAPTERS) - 1 else None

    # Load content
    file_path = os.path.join(CHAPTERS_DIR, f"{chapter_id}.md")
    if not os.path.exists(file_path):
        content = "# Content Coming Soon"
    else:
        with open(file_path, 'r') as f:
            content = f.read()

    # Convert Markdown
    html_content = markdown.markdown(content, extensions=['fenced_code', 'codehilite', 'tables'])

    return templates.TemplateResponse("chapter.html", {
        "request": request,
        "content": html_content,
        "chapters": CHAPTERS,
        "current_chapter": CHAPTERS[current_index],
        "prev_chapter": prev_chapter,
        "next_chapter": next_chapter
    })
