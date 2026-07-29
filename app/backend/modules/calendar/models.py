"""Calendar module data models."""

from pydantic import BaseModel


class CalendarDay(BaseModel):
    """A single day in the calendar view."""

    date: str
    posts: list[dict]
    is_best_day: bool = False
    is_slow_day: bool = False
    day_name: str = ""
    day_number: int = 0


class SchedulePostRequest(BaseModel):
    """Request to schedule a post to a date."""

    scheduled_date: str
