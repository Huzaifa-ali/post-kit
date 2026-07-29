"""Post-kit desktop app — FastAPI entry point with full startup lifecycle."""

import logging
from contextlib import asynccontextmanager
from datetime import datetime
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
from backend.modules.calendar import service as calendar_service
from backend.modules.images.router import router as images_router
from backend.modules.images import service as images_service
from backend.modules.brand.router import router as brand_router
from backend.modules.brand import service as brand_service
from backend.modules.analytics.router import router as analytics_router
from backend.modules.analytics import service as analytics_service
from backend.modules.credits.router import router as credits_router
from backend.modules.notifications.router import router as notifications_router
from backend.modules.settings.router import router as settings_router
from backend.mcp.registry import has_image_server

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
app.include_router(analytics_router)
app.include_router(credits_router)
app.include_router(notifications_router)
app.include_router(settings_router)


def _get_nav_context(bridge: PostKitBridge) -> list[dict]:
    """Build sidebar navigation from bridge config."""
    groups = [
        {"label": "Create", "items": [
            {"id": "content", "label": "Content", "icon": "✦", "url": "/content"},
        ]},
        {"label": "Manage", "items": [
            {"id": "library", "label": "Library", "icon": "📚", "url": "/library"},
            {"id": "calendar", "label": "Calendar", "icon": "📅", "url": "/calendar"},
        ]},
        {"label": "Settings", "items": [
            {"id": "brand", "label": "Brand", "icon": "🎨", "url": "/brand"},
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


def _page_context(bridge: PostKitBridge, current_page: str) -> dict:
    """Build the full template context for a page."""
    return {
        "nav_groups": _get_nav_context(bridge),
        "current_page": current_page,
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



@app.get("/calendar")
async def calendar_page(request: Request):
    """Calendar page with month view and queue."""
    bridge = PostKitBridge(get_postkit_root())
    queue = await calendar_service.get_queue()
    now = datetime.now()
    context = {
        "queue": queue,
        "year": now.year,
        "month_name": now.strftime("%B"),
        **_page_context(bridge, "calendar"),
    }
    return templates.TemplateResponse(request, "calendar.html", context)


@app.get("/images")
async def images_page(request: Request):
    """Images page with media library."""
    bridge = PostKitBridge(get_postkit_root())
    images = images_service.list_images()
    context = {
        "images": images,
        "mcp_available": has_image_server(),
        **_page_context(bridge, "images"),
    }
    return templates.TemplateResponse(request, "images.html", context)


@app.get("/brand")
async def brand_page(request: Request):
    """Brand page for niche file editing."""
    bridge = PostKitBridge(get_postkit_root())
    niche_files = brand_service.list_niche_files(bridge)
    context = {
        "niche_files": niche_files,
        **_page_context(bridge, "brand"),
    }
    return templates.TemplateResponse(request, "brand.html", context)


@app.get("/analytics")
async def analytics_page(request: Request):
    """Analytics dashboard page."""
    bridge = PostKitBridge(get_postkit_root())
    dashboard = await analytics_service.get_dashboard_data()
    context = {
        "dashboard": dashboard,
        **_page_context(bridge, "analytics"),
    }
    return templates.TemplateResponse(request, "analytics.html", context)


@app.get("/settings")
async def settings_page(request: Request):
    """Settings page."""
    bridge = PostKitBridge(get_postkit_root())
    config = load_config()
    context = {
        "config": config,
        "postkit_version": bridge.get_version(),
        "niche_version": bridge.get_niche_version(),
        "is_update_available": bridge.get_version() != bridge.get_niche_version(),
        **_page_context(bridge, "settings"),
    }
    return templates.TemplateResponse(request, "settings.html", context)
