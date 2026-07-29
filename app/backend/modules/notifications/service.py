"""Notifications service — activity feed and alerts."""

from datetime import datetime

from backend.core.database import get_db


async def create_notification(type: str, message: str, link: str | None = None) -> int:
    """Create a new notification. Returns its ID."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "INSERT INTO notifications (type, message, link, created_at) VALUES (?, ?, ?, ?)",
            (type, message, link, datetime.now().isoformat()),
        )
        await db.commit()
        return cursor.lastrowid
    finally:
        await db.close()


async def get_notifications(limit: int = 20) -> list[dict]:
    """Get recent notifications, unread first."""
    db = await get_db()
    try:
        cursor = await db.execute(
            """SELECT * FROM notifications
               ORDER BY is_read ASC, created_at DESC
               LIMIT ?""",
            (limit,),
        )
        rows = await cursor.fetchall()
    finally:
        await db.close()
    return [dict(row) for row in rows]


async def mark_as_read(notification_id: int) -> None:
    """Mark a notification as read."""
    db = await get_db()
    try:
        await db.execute(
            "UPDATE notifications SET is_read = 1 WHERE id = ?",
            (notification_id,),
        )
        await db.commit()
    finally:
        await db.close()


async def get_unread_count() -> int:
    """Get count of unread notifications."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT COUNT(*) as cnt FROM notifications WHERE is_read = 0"
        )
        row = await cursor.fetchone()
    finally:
        await db.close()
    return row["cnt"] if row else 0
