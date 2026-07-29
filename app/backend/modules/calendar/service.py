"""Calendar service — scheduling and cadence logic."""

from datetime import date, datetime
from calendar import monthrange

from backend.core.database import get_db


async def get_month_posts(year: int, month: int) -> list[dict]:
    """Get all posts for a given month from the index."""
    month_start = f"{year}-{month:02d}-01"
    month_end = f"{year}-{month:02d}-{monthrange(year, month)[1]}"
    db = await get_db()
    try:
        cursor = await db.execute(
            """SELECT * FROM posts
               WHERE created_at >= ? AND created_at <= ?
               ORDER BY created_at ASC""",
            (month_start, month_end + "T23:59:59"),
        )
        rows = await cursor.fetchall()
    finally:
        await db.close()
    return [dict(row) for row in rows]


def build_calendar_days(
    year: int, month: int, posts: list[dict], cadence: dict | None
) -> list[dict]:
    """Build calendar day objects with posts mapped and cadence overlay."""
    num_days = monthrange(year, month)[1]
    best_days = cadence.get("best_days", []) if cadence else []
    slow_days = cadence.get("slow_days", []) if cadence else []

    days = []
    for day_num in range(1, num_days + 1):
        current_date = date(year, month, day_num)
        day_name = current_date.strftime("%A").lower()
        date_str = current_date.isoformat()

        day_posts = [
            p for p in posts if p.get("created_at", "").startswith(date_str)
        ]

        days.append({
            "date": date_str,
            "posts": day_posts,
            "is_best_day": day_name in best_days,
            "is_slow_day": day_name in slow_days,
            "day_name": day_name,
            "day_number": day_num,
        })
    return days


async def schedule_post(post_id: str, scheduled_date: str) -> None:
    """Assign a scheduled date to a post."""
    db = await get_db()
    try:
        await db.execute(
            "UPDATE posts SET created_at = ?, updated_at = ? WHERE id = ?",
            (scheduled_date, datetime.now().isoformat(), post_id),
        )
        await db.commit()
    finally:
        await db.close()


async def get_queue() -> list[dict]:
    """Get approved posts not yet published (the queue)."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT * FROM posts WHERE status = 'approved' ORDER BY created_at ASC"
        )
        rows = await cursor.fetchall()
    finally:
        await db.close()
    return [dict(row) for row in rows]
