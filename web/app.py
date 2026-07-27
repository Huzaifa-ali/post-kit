"""post-kit Web UI — read-only post viewer + config editor."""

from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .services.db import init_db
from .routes import dashboard, onboarding, posts, settings, api, how_it_works

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
STATIC_DIR = BASE_DIR / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="post-kit", docs_url=None, redoc_url=None, lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

app.include_router(dashboard.router)
app.include_router(onboarding.router)
app.include_router(posts.router)
app.include_router(settings.router)
app.include_router(api.router)
app.include_router(how_it_works.router)


@app.get("/")
async def root():
    niche_file = PROJECT_ROOT / "my-niche" / "niche.yaml"
    if niche_file.exists():
        return RedirectResponse(url="/dashboard", status_code=302)
    return RedirectResponse(url="/onboarding", status_code=302)
