"""Brand module routes — niche file listing and editing."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.config import get_postkit_root
from backend.core.bridge import PostKitBridge
from backend.modules.brand import service

router = APIRouter(prefix="/api/brand", tags=["brand"])


class SaveFileRequest(BaseModel):
    content: str


@router.get("/files")
async def list_files() -> list[dict]:
    """List all niche files."""
    bridge = PostKitBridge(get_postkit_root())
    return service.list_niche_files(bridge)


@router.get("/files/{filename}")
async def get_file(filename: str) -> dict:
    """Get content of a niche file."""
    bridge = PostKitBridge(get_postkit_root())
    content = service.get_file_content(bridge, filename)
    if content is None:
        raise HTTPException(status_code=404, detail="File not found")
    return {"filename": filename, "content": content}


@router.put("/files/{filename}")
async def save_file(filename: str, request: SaveFileRequest) -> dict[str, str]:
    """Save edited content to a niche file."""
    bridge = PostKitBridge(get_postkit_root())
    service.save_file_content(bridge, filename, request.content)
    return {"status": "saved"}
