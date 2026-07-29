"""Calendar module routes — month view and scheduling."""

from fastapi import APIRouter, HTTPException

from backend.modules.calendar import service
from backend.modules.calendar.models import SchedulePostRequest

router = APIRouter(prefix="/api/calendar", tags=["calendar"])


@router.get("/month/{year}/{month}")
async def get_month(year: int, month: int) -> dict:
    """Get calendar data for a month."""
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Invalid month")
    posts = await service.get_month_posts(year, month)
    days = service.build_calendar_days(year, month, posts, None)
    return {"year": year, "month": month, "days": days}


@router.get("/queue")
async def get_queue() -> list[dict]:
    """Get the post queue (approved, not yet published)."""
    return await service.get_queue()


@router.put("/schedule/{post_id}")
async def schedule_post(post_id: str, request: SchedulePostRequest) -> dict[str, str]:
    """Schedule a post to a specific date."""
    await service.schedule_post(post_id, request.scheduled_date)
    return {"status": "scheduled"}
