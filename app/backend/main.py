"""Post-kit desktop app — FastAPI entry point with full startup lifecycle."""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.config import get_postkit_root, load_config
from backend.core.bridge import PostKitBridge
from backend.core.database import init_db, is_index_stale
from backend.modules.library.router import router as library_router
from backend.modules.library import service as library_service
from backend.modules.content.router import router as content_router
from backend.modules.calendar.router import router as calendar_router
from backend.modules.images.router import router as images_router
from backend.modules.brand.router import router as brand_router

logger = logging.getLogger(__name__)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

templates = Jinja2Templates(
    directory=[
        str(FRONTEND_DIR / "templates"),
        str(FRONTEND_DIR),
    ]
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: init DB, check index, log readiness."""
    await init_db()
    bridge = PostKitBridge(get_postkit_root())
    posts_path = bridge.get_posts_path()
    if posts_path.exists() and await is_index_stale(posts_path):
        count = await library_service.rebuild_index(posts_path)
        logger.info(f"Index rebuilt: {count} posts indexed")
    logger.info("post-kit app ready")
    yield


app = FastAPI(title="post-kit", docs_url=None, redoc_url=None, lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")

app.include_router(library_router)
app.include_router(content_router)
app.include_router(calendar_router)
app.include_router(images_router)
app.include_router(brand_router)


def _get_nav_context(bridge: PostKitBridge) -> list[dict]:
    """Build sidebar navigation from bridge config."""
    groups = [
        {"label": "Create", "items": [
            {"id": "content", "label": "Content", "icon": "✦", "url": "/content"},
        ]},
        {"label": "Manage", "items": [
            {"id": "library", "label": "Library", "icon": "📚", "url": "/library"},
        ]},
        {"label": "Settings", "items": [
            {"id": "settings", "label": "Settings", "icon": "⚙", "url": "/settings"},
        ]},
    ]
    modules = bridge.get_active_modules()
    if any(m in modules for m in ["visual-system", "image-prompts"]):
        groups[0]["items"].append(
            {"id": "images", "label": "Images", "icon": "🖼", "url": "/images"}
        )
    if "analytics" in modules:
        groups.insert(2, {"label": "Insights", "items": [
            {"id": "analytics", "label": "Analytics", "icon": "📊", "url": "/analytics"},
        ]})
    return groups


def _get_credits_context() -> dict:
    """Load credits/plan info from config."""
    config = load_config()
    plan = config.get("plan", {"name": "Free", "limit": 100})
    usage = config.get("usage", {"count": 0})
    limit = plan.get("limit", 100)
    count = usage.get("count", 0)
    return {
        "plan_name": plan.get("name", "Free"),
        "usage_count": count,
        "usage_limit": limit,
        "usage_percent": min(100, int(count / max(limit, 1) * 100)),
    }


def _page_context(bridge: PostKitBridge, current_page: str) -> dict:
    """Build the full template context for a page."""
    return {
        "nav_groups": _get_nav_context(bridge),
        "current_page": current_page,
        **_get_credits_context(),
    }


@app.get("/api/health")
async def health_check() -> dict[str, str]:
    """Health endpoint for Tauri readiness check."""
    return {"status": "ok"}


@app.get("/")
async def root() -> RedirectResponse:
    """Redirect to content (if onboarded) or onboarding."""
    bridge = PostKitBridge(get_postkit_root())
    if not bridge.is_onboarded():
        return RedirectResponse(url="/onboarding", status_code=302)
    return RedirectResponse(url="/content", status_code=302)


@app.get("/onboarding")
async def onboarding_page(request: Request):
    """Onboarding page (standalone, no sidebar)."""
    return templates.TemplateResponse(request, "onboarding.html")


@app.get("/library")
async def library_page(request: Request):
    """Library page showing all posts."""
    bridge = PostKitBridge(get_postkit_root())
    posts = await library_service.get_posts()
    context = {"posts": posts, **_page_context(bridge, "library")}
    return templates.TemplateResponse(request, "library.html", context)


@app.get("/content")
async def content_page(request: Request):
    """Content creation page with chat interface."""
    bridge = PostKitBridge(get_postkit_root())
    context = {"adapter_available": False, **_page_context(bridge, "content")}
    return templates.TemplateResponse(request, "content.html", context)
