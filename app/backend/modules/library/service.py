"""Library service — post indexing, search, and status management."""

import hashlib
from datetime import datetime
from pathlib import Path

import yaml

from backend.core.database import get_db, set_last_index_time
from backend.core.models import PostStatus


def _generate_post_id(path: str) -> str:
    """Generate a stable ID from file path."""
    return hashlib.md5(path.encode()).hexdigest()[:12]


def _extract_front_matter(content: str) -> tuple[dict, str]:
    """Extract YAML front matter from markdown. Returns (metadata, body)."""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    try:
        metadata = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        metadata = {}
    body = parts[2].strip()
    return metadata, body


def _extract_title(content: str) -> str:
    """Extract first non-empty line as title (the hook)."""
    for line in content.split("\n"):
        stripped = line.strip().lstrip("#").strip()
        if stripped:
            return stripped[:120]
    return "(untitled)"


async def rebuild_index(posts_path: Path) -> int:
    """Scan posts directory and rebuild the SQLite index. Returns count."""
    if not posts_path.exists():
        return 0

    count = 0
    db = await get_db()
    try:
        await db.execute("DELETE FROM posts")
        for md_file in posts_path.rglob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            metadata, body = _extract_front_matter(content)
            title = _extract_title(body)
            relative_path = str(md_file.relative_to(posts_path))
            post_id = _generate_post_id(relative_path)

            created_at = metadata.get(
                "created",
                datetime.fromtimestamp(md_file.stat().st_mtime).isoformat(),
            )

            await db.execute(
                """INSERT OR REPLACE INTO posts
                   (id, path, title, status, pillar, platform, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    post_id,
                    relative_path,
                    title,
                    metadata.get("status", PostStatus.PUBLISHED),
                    metadata.get("pillar"),
                    metadata.get("platform"),
                    str(created_at),
                ),
            )
            count += 1
        await db.commit()
    finally:
        await db.close()

    await set_last_index_time()
    return count


async def get_posts(
    status: PostStatus | None = None,
    pillar: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[dict]:
    """Get posts from index with optional filters."""
    query = "SELECT * FROM posts WHERE 1=1"
    params: list = []

    if status:
        query += " AND status = ?"
        params.append(status)
    if pillar:
        query += " AND pillar = ?"
        params.append(pillar)

    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    db = await get_db()
    try:
        cursor = await db.execute(query, params)
        rows = await cursor.fetchall()
    finally:
        await db.close()
    return [dict(row) for row in rows]


async def get_post_by_id(post_id: str) -> dict | None:
    """Get a single post from index."""
    db = await get_db()
    try:
        cursor = await db.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        row = await cursor.fetchone()
    finally:
        await db.close()
    return dict(row) if row else None


def read_post_content(posts_path: Path, relative_path: str) -> str | None:
    """Read the full file content of a post from disk."""
    filepath = posts_path / relative_path
    if not filepath.exists():
        return None
    return filepath.read_text(encoding="utf-8")


async def update_post_status(post_id: str, status: PostStatus) -> None:
    """Update a post's status in the index."""
    db = await get_db()
    try:
        await db.execute(
            "UPDATE posts SET status = ?, updated_at = ? WHERE id = ?",
            (status, datetime.now().isoformat(), post_id),
        )
        await db.commit()
    finally:
        await db.close()


async def get_post_count() -> int:
    """Get total post count."""
    db = await get_db()
    try:
        cursor = await db.execute("SELECT COUNT(*) as cnt FROM posts")
        row = await cursor.fetchone()
    finally:
        await db.close()
    return row["cnt"] if row else 0
