"""Post-kit desktop app — FastAPI entry point."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    yield


app = FastAPI(title="post-kit", docs_url=None, redoc_url=None, lifespan=lifespan)

# Static files will be mounted once frontend directory exists
# app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")


@app.get("/api/health")
async def health_check():
    """Health endpoint for Tauri readiness check."""
    return {"status": "ok"}
