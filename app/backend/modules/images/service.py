"""Images service — media library and file management."""

import json
from datetime import datetime
from pathlib import Path

from backend.config import APP_DIR

MEDIA_DIR = APP_DIR / "data" / "media"
MANIFEST_PATH = MEDIA_DIR / "manifest.json"


def _ensure_media_dir() -> None:
    """Ensure media directory exists."""
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)


def _load_manifest() -> list[dict]:
    """Load the image manifest."""
    if not MANIFEST_PATH.exists():
        return []
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _save_manifest(manifest: list[dict]) -> None:
    """Save the image manifest."""
    _ensure_media_dir()
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def list_images(tag: str | None = None) -> list[dict]:
    """List all images, optionally filtered by tag."""
    manifest = _load_manifest()
    if tag:
        return [img for img in manifest if tag in img.get("tags", [])]
    return manifest


def save_uploaded_image(
    filename: str, content: bytes, tags: list[str] | None = None
) -> dict:
    """Save an uploaded image to media directory."""
    _ensure_media_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = f"{timestamp}_{filename}"
    filepath = MEDIA_DIR / safe_name
    filepath.write_bytes(content)

    entry = {
        "filename": safe_name,
        "original_name": filename,
        "created_at": datetime.now().isoformat(),
        "tags": tags or [],
        "associated_post": None,
        "size_bytes": len(content),
    }

    manifest = _load_manifest()
    manifest.append(entry)
    _save_manifest(manifest)
    return entry


def delete_image(filename: str) -> bool:
    """Delete an image from media library."""
    filepath = MEDIA_DIR / filename
    if filepath.exists():
        filepath.unlink()
    manifest = _load_manifest()
    manifest = [img for img in manifest if img["filename"] != filename]
    _save_manifest(manifest)
    return True


def get_image_path(filename: str) -> Path | None:
    """Get full path to an image file."""
    filepath = MEDIA_DIR / filename
    return filepath if filepath.exists() else None
