"""SQLite database — rebuildable index over the filesystem."""

import aiosqlite
from pathlib import Path
from datetime import datetime

from backend.config import APP_DIR

DB_PATH = APP_DIR / "data" / "postkit.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS posts (
    id TEXT PRIMARY KEY,
    path TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'published',
    pillar TEXT,
    platform TEXT,
    created_at TEXT NOT NULL,
    published_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    message TEXT NOT NULL,
    is_read INTEGER NOT NULL DEFAULT 0,
    link TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


async def get_db() -> aiosqlite.Connection:
    """Get a database connection."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = await aiosqlite.connect(str(DB_PATH))
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA journal_mode=WAL")
    return db


async def init_db() -> None:
    """Initialize database schema."""
    db = await get_db()
    try:
        await db.executescript(SCHEMA)
        await db.commit()
    finally:
        await db.close()


async def get_last_index_time() -> datetime | None:
    """Get the last time the index was built."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT value FROM meta WHERE key = 'last_index_build'"
        )
        row = await cursor.fetchone()
        if not row:
            return None
        return datetime.fromisoformat(row["value"])
    finally:
        await db.close()


async def set_last_index_time() -> None:
    """Record the current time as last index build."""
    now = datetime.now().isoformat()
    db = await get_db()
    try:
        await db.execute(
            "INSERT OR REPLACE INTO meta (key, value) VALUES ('last_index_build', ?)",
            (now,),
        )
        await db.commit()
    finally:
        await db.close()


async def is_index_stale(posts_path: Path) -> bool:
    """Check if any file in posts/ is newer than last index build."""
    last_build = await get_last_index_time()
    if last_build is None:
        return True
    if not posts_path.exists():
        return False
    for md_file in posts_path.rglob("*.md"):
        file_mtime = datetime.fromtimestamp(md_file.stat().st_mtime)
        if file_mtime > last_build:
            return True
    return False
