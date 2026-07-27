"""API routes — save/retrieve posts programmatically. Used by CLI tools to push generated content."""

from fastapi import APIRouter
from pydantic import BaseModel

from ..services import db

router = APIRouter(prefix="/api")


class SavePostRequest(BaseModel):
    topic: str
    content: str
    platform: str = "linkedin"
    post_type: str = "opinion"


class UpdatePostRequest(BaseModel):
    content: str
    status: str = "completed"


@router.get("/posts")
async def api_list_posts(limit: int = 50, offset: int = 0):
    """List all posts."""
    posts = await db.get_all_posts(limit, offset)
    count = await db.get_posts_count()
    return {"posts": posts, "total": count}


@router.get("/posts/{post_id}")
async def api_get_post(post_id: int):
    """Get a single post with pipeline runs."""
    post = await db.get_post(post_id)
    if not post:
        return {"error": "Not found"}
    runs = await db.get_pipeline_runs(post_id)
    return {"post": post, "pipeline_runs": runs}


@router.post("/posts")
async def api_save_post(req: SavePostRequest):
    """Save a new post directly (used by CLI tools to push generated content)."""
    post_id = await db.create_post(
        topic=req.topic,
        platform=req.platform,
        post_type=req.post_type,
    )
    await db.update_post_content(post_id, req.content, "completed")
    return {"post_id": post_id, "status": "saved", "url": f"/posts/{post_id}"}


@router.put("/posts/{post_id}")
async def api_update_post(post_id: int, req: UpdatePostRequest):
    """Update an existing post's content."""
    post = await db.get_post(post_id)
    if not post:
        return {"error": "Not found"}
    await db.update_post_content(post_id, req.content, req.status)
    return {"post_id": post_id, "status": "updated"}


@router.delete("/posts/{post_id}")
async def api_delete_post(post_id: int):
    """Delete a post."""
    await db.delete_post(post_id)
    return {"status": "deleted"}


@router.get("/settings")
async def api_get_settings():
    """Get all settings."""
    settings = await db.get_all_settings()
    return {"settings": settings}
