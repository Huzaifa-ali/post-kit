"""Images module routes — media library and upload."""

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse

from backend.modules.images import service
from backend.modules.images.models import UploadResponse, GenerateImageRequest

router = APIRouter(prefix="/api/images", tags=["images"])


@router.get("/list")
async def list_images(tag: str | None = None) -> list[dict]:
    """List all images in media library."""
    return service.list_images(tag=tag)


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)) -> UploadResponse:
    """Upload an image to the media library."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large (max 10MB)")
    entry = service.save_uploaded_image(file.filename, content)
    return UploadResponse(
        filename=entry["filename"],
        path=f"/api/images/file/{entry['filename']}",
    )


@router.get("/file/{filename}")
async def get_image_file(filename: str) -> FileResponse:
    """Serve an image file."""
    filepath = service.get_image_path(filename)
    if not filepath:
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(filepath)


@router.delete("/{filename}")
async def delete_image(filename: str) -> dict[str, str]:
    """Delete an image from the library."""
    service.delete_image(filename)
    return {"status": "deleted"}


@router.post("/generate")
async def generate_image(request: GenerateImageRequest) -> dict[str, str]:
    """Generate an image via MCP (stub)."""
    return {
        "status": "not_configured",
        "message": "MCP image server not configured. Add one in Settings.",
    }
