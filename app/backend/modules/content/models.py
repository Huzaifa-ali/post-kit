"""Content module data models."""

from pydantic import BaseModel, Field


class SendMessageRequest(BaseModel):
    """Request to send a message to the AI adapter."""
    message: str = Field(min_length=1, max_length=5000)
    session_id: str | None = None


class SessionResponse(BaseModel):
    """Response when a new session is created."""
    session_id: str


class AdapterStatusResponse(BaseModel):
    """Response for adapter availability check."""
    available: bool
    adapter: str
    message: str
