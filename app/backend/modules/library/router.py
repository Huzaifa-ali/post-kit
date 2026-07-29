"""Library module routes — post listing, detail, status updates."""

from fastapi import APIRouter, HTTPException

from backend.config import get_postkit_root
from backend.core.bridge import PostKitBridge
from backend.core.models import PostStatus
from backend.modules.library import service
from backend.modules.library.models import PostSummary, UpdatePostRequest

router = APIRouter(prefix="/api/library", tags=["library"])


@router.get("/posts")
async def list_posts(
    status: PostStatus | None = None,
    pillar: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[PostSummary]:
    """List posts with optional filters."""
    posts = await service.get_posts(
        status=status, pillar=pillar, limit=limit, offset=offset
    )
    return [PostSummary(**p) for p in posts]


@router.get("/posts/{post_id}")
async def get_post(post_id: str) -> dict:
    """Get a single post by ID with full file content."""
    post = await service.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    bridge = PostKitBridge(get_postkit_root())
    posts_path = bridge.get_posts_path()
    content = service.read_post_content(posts_path, post["path"])
    post["content"] = content or ""
    return post


@router.put("/posts/{post_id}")
async def update_post(post_id: str, request: UpdatePostRequest) -> dict[str, str]:
    """Update post status."""
    post = await service.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if request.status:
        await service.update_post_status(post_id, request.status)
    return {"status": "updated"}


@router.get("/count")
async def post_count() -> dict[str, int]:
    """Get total post count."""
    count = await service.get_post_count()
    return {"count": count}
