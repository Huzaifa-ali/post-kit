"""SQLite database service for post-kit."""

import aiosqlite
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "postkit.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    content TEXT NOT NULL,
    platform TEXT NOT NULL DEFAULT 'linkedin',
    post_type TEXT NOT NULL DEFAULT 'opinion',
    hashtags TEXT,
    image_prompt TEXT,
    video_prompt TEXT,
    references_used TEXT,
    cli_tool TEXT NOT NULL DEFAULT 'kiro',
    saved_to TEXT,
    status TEXT NOT NULL DEFAULT 'completed',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""

MIGRATIONS = [
    "ALTER TABLE posts ADD COLUMN image_prompt TEXT",
    "ALTER TABLE posts ADD COLUMN references_used TEXT",
    "ALTER TABLE posts ADD COLUMN cli_tool TEXT NOT NULL DEFAULT 'kiro'",
    "ALTER TABLE posts ADD COLUMN saved_to TEXT",
    "ALTER TABLE posts ADD COLUMN hashtags TEXT",
    "ALTER TABLE posts ADD COLUMN video_prompt TEXT",
]


async def get_db() -> aiosqlite.Connection:
    """Get database connection."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = await aiosqlite.connect(str(DB_PATH))
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA journal_mode=WAL")
    await db.execute("PRAGMA foreign_keys=ON")
    return db


async def init_db():
    """Initialize database with schema."""
    db = await get_db()
    try:
        await db.executescript(SCHEMA)
        # Run migrations (ignore errors for already-existing columns)
        for migration in MIGRATIONS:
            try:
                await db.execute(migration)
            except Exception:
                pass
        await db.commit()
    finally:
        await db.close()


# --- Settings ---

async def get_setting(key: str, default: str = "") -> str:
    db = await get_db()
    try:
        cursor = await db.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = await cursor.fetchone()
        return row["value"] if row else default
    finally:
        await db.close()


async def set_setting(key: str, value: str):
    db = await get_db()
    try:
        await db.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, value),
        )
        await db.commit()
    finally:
        await db.close()


async def get_all_settings() -> dict:
    db = await get_db()
    try:
        cursor = await db.execute("SELECT key, value FROM settings")
        rows = await cursor.fetchall()
        return {row["key"]: row["value"] for row in rows}
    finally:
        await db.close()


# --- Posts ---

async def save_post(
    topic: str,
    content: str,
    platform: str = "linkedin",
    post_type: str = "opinion",
    hashtags: str = None,
    image_prompt: str = None,
    video_prompt: str = None,
    references_used: str = None,
    cli_tool: str = "kiro",
    saved_to: str = None,
) -> int:
    """Save a post with full metadata. Returns post ID. Also writes to disk if saved_to is set."""
    db = await get_db()
    try:
        cursor = await db.execute(
            """INSERT INTO posts (topic, content, platform, post_type, hashtags, image_prompt, video_prompt, references_used, cli_tool, saved_to, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'completed')""",
            (topic, content, platform, post_type, hashtags, image_prompt, video_prompt, references_used, cli_tool, saved_to),
        )
        await db.commit()
        post_id = cursor.lastrowid
    finally:
        await db.close()

    # Write markdown file to disk
    if saved_to:
        file_path = DB_PATH.parent.parent / saved_to
        file_path.parent.mkdir(parents=True, exist_ok=True)

        md_content = f"""---
topic: {topic}
platform: {platform}
type: {post_type}
cli: {cli_tool}
---

{content}
"""
        if hashtags:
            md_content += f"\n{hashtags}\n"
        if image_prompt:
            md_content += f"\n---\n## Image Prompt\n{image_prompt}\n"
        if video_prompt:
            md_content += f"\n---\n## Video Prompt\n{video_prompt}\n"
        if references_used:
            md_content += f"\n---\n## References\n{references_used}\n"

        file_path.write_text(md_content, encoding="utf-8")

    return post_id


async def get_post(post_id: int) -> dict | None:
    db = await get_db()
    try:
        cursor = await db.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()


async def get_all_posts(limit: int = 50, offset: int = 0) -> list[dict]:
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT * FROM posts ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, offset),
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        await db.close()


async def get_posts_count() -> int:
    db = await get_db()
    try:
        cursor = await db.execute("SELECT COUNT(*) as cnt FROM posts")
        row = await cursor.fetchone()
        return row["cnt"]
    finally:
        await db.close()


async def delete_post(post_id: int):
    db = await get_db()
    try:
        await db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        await db.commit()
    finally:
        await db.close()
