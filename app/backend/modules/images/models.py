"""Images module data models."""

from pydantic import BaseModel, Field


class ImageMetadata(BaseModel):
    """Metadata for a stored image."""
    filename: str
    original_name: str = ""
    created_at: str = ""
    tags: list[str] = []
    associated_post: str | None = None
    size_bytes: int = 0


class UploadResponse(BaseModel):
    """Response after uploading an image."""
    filename: str
    path: str


class GenerateImageRequest(BaseModel):
    """Request to generate an image via MCP."""
    prompt: str = Field(min_length=1, max_length=2000)
    post_id: str | None = None
