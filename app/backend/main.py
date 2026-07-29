"""Post-kit desktop app — FastAPI entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    yield


app = FastAPI(title="post-kit", docs_url=None, redoc_url=None, lifespan=lifespan)


@app.get("/api/health")
async def health_check() -> dict[str, str]:
    """Health endpoint for Tauri readiness check."""
    return {"status": "ok"}
