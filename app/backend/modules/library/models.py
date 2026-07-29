"""Library module data models."""

from pydantic import BaseModel, ConfigDict

from backend.core.models import PostStatus


class PostSummary(BaseModel):
    """Post card data for list views."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    status: PostStatus
    pillar: str | None = None
    platform: str | None = None
    created_at: str
    path: str


class PostDetail(PostSummary):
    """Full post data for editor view."""

    content: str


class UpdatePostRequest(BaseModel):
    """Request to update a post's content or status."""

    content: str | None = None
    status: PostStatus | None = None
