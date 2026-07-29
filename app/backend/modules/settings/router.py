"""Settings module routes — technical configuration."""

from fastapi import APIRouter
from pydantic import BaseModel

from backend.config import load_config, save_config, get_postkit_root
from backend.core.bridge import PostKitBridge
from backend.core.database import init_db
from backend.modules.library import service as library_service

router = APIRouter(prefix="/api/settings", tags=["settings"])


class UpdateSettingsRequest(BaseModel):
    adapter: str | None = None
    postkit_path: str | None = None
    theme: str | None = None


@router.get("")
async def get_settings() -> dict:
    """Get current app configuration."""
    config = load_config()
    bridge = PostKitBridge(get_postkit_root())
    return {
        "config": config,
        "postkit_version": bridge.get_version(),
        "niche_version": bridge.get_niche_version(),
        "is_update_available": _is_update_available(bridge),
    }


@router.put("")
async def update_settings(request: UpdateSettingsRequest) -> dict[str, str]:
    """Update app configuration."""
    config = load_config()
    if request.adapter is not None:
        config["adapter"] = request.adapter
    if request.postkit_path is not None:
        config["postkit_path"] = request.postkit_path
    if request.theme is not None:
        config["theme"] = request.theme
    save_config(config)
    return {"status": "saved"}


@router.post("/rebuild")
async def rebuild_index() -> dict[str, int]:
    """Trigger a full index rebuild."""
    bridge = PostKitBridge(get_postkit_root())
    posts_path = bridge.get_posts_path()
    count = await library_service.rebuild_index(posts_path)
    return {"rebuilt": count}


def _is_update_available(bridge: PostKitBridge) -> bool:
    """Check if post-kit version is ahead of niche version."""
    pk_version = bridge.get_version()
    niche_version = bridge.get_niche_version()
    if not pk_version or not niche_version:
        return False
    return pk_version != niche_version
