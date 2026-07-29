"""Notifications module routes — activity feed."""

from fastapi import APIRouter

from backend.modules.notifications import service

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


@router.get("")
async def list_notifications(limit: int = 20) -> list[dict]:
    """Get recent notifications."""
    return await service.get_notifications(limit=limit)


@router.put("/{notification_id}/read")
async def mark_read(notification_id: int) -> dict[str, str]:
    """Mark a notification as read."""
    await service.mark_as_read(notification_id)
    return {"status": "read"}


@router.get("/unread-count")
async def unread_count() -> dict[str, int]:
    """Get unread notification count for badge."""
    count = await service.get_unread_count()
    return {"count": count}
