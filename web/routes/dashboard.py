"""Dashboard route — home page after setup."""

import yaml
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from .helpers import templates, MY_NICHE_DIR, is_setup_complete
from ..services import db

router = APIRouter()


def get_niche_info() -> dict | None:
    """Load niche.yaml data."""
    niche_file = MY_NICHE_DIR / "niche.yaml"
    if not niche_file.exists():
        return None
    with open(niche_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_active_modules() -> list[str]:
    """Get list of active module files in my-niche."""
    module_names = [
        "visual-system", "memes", "news-scout", "video-content",
        "image-prompts", "analytics", "repurpose", "carousel"
    ]
    return [mod for mod in module_names if (MY_NICHE_DIR / f"{mod}.md").exists()]


@router.get("/dashboard")
async def dashboard(request: Request):
    if not is_setup_complete():
        return RedirectResponse(url="/onboarding", status_code=302)

    niche = get_niche_info()
    active_modules = get_active_modules()
    total_posts = await db.get_posts_count()
    recent_posts = await db.get_all_posts(limit=5)

    return templates.TemplateResponse(request, "dashboard.html", {
        "niche": niche,
        "recent_posts": recent_posts,
        "active_modules": active_modules,
        "total_posts": total_posts,
        "page": "dashboard",
    })
