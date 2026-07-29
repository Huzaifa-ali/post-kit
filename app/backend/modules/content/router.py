"""Content module routes — chat and scout endpoints."""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from backend.modules.content.models import (
    AdapterStatusResponse,
    SendMessageRequest,
    SessionResponse,
)

router = APIRouter(prefix="/api/content", tags=["content"])


@router.post("/session")
async def start_session() -> SessionResponse:
    """Start a new content creation session."""
    # Will be wired to ContentService via dependency injection in main.py
    return SessionResponse(session_id="not-configured")


@router.post("/send")
async def send_message(request: SendMessageRequest) -> StreamingResponse:
    """Send a message and get streaming response via SSE."""

    async def event_stream():
        yield f"data: Received: {request.message}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/scout")
async def trigger_scout() -> dict[str, str]:
    """Trigger a news scout via the adapter."""
    return {
        "status": "not_configured",
        "message": "Adapter not yet wired. Will use adapter session when configured.",
    }


@router.get("/adapter-status")
async def adapter_status() -> AdapterStatusResponse:
    """Check if the AI adapter is available."""
    # Will be wired to ContentService via dependency injection in main.py
    return AdapterStatusResponse(
        available=False,
        adapter="kiro",
        message="Adapter not yet configured",
    )
