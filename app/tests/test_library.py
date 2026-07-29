"""Tests for the library module."""

import pytest
from pathlib import Path

from backend.core import database
from backend.modules.library import service


@pytest.fixture(autouse=True)
def use_temp_db(tmp_path, monkeypatch):
    """Use a temporary database."""
    test_db = tmp_path / "test.db"
    monkeypatch.setattr(database, "DB_PATH", test_db)


@pytest.fixture
def posts_dir(tmp_path) -> Path:
    """Create test posts on disk."""
    month_dir = tmp_path / "posts" / "2026-july"
    month_dir.mkdir(parents=True)

    (month_dir / "test-post.md").write_text(
        "---\nstatus: draft\npillar: News\nplatform: linkedin\n---\nBreaking: AI news today\nMore content here.",
        encoding="utf-8",
    )
    (month_dir / "second-post.md").write_text(
        "This has no front matter\nJust plain content",
        encoding="utf-8",
    )
    return tmp_path / "posts"


@pytest.mark.asyncio
async def test_rebuild_index(posts_dir):
    await database.init_db()
    count = await service.rebuild_index(posts_dir)
    assert count == 2


@pytest.mark.asyncio
async def test_rebuild_empty_dir(tmp_path):
    await database.init_db()
    count = await service.rebuild_index(tmp_path / "nonexistent")
    assert count == 0


@pytest.mark.asyncio
async def test_get_posts_returns_all(posts_dir):
    await database.init_db()
    await service.rebuild_index(posts_dir)
    posts = await service.get_posts()
    assert len(posts) == 2


@pytest.mark.asyncio
async def test_get_posts_filter_by_status(posts_dir):
    await database.init_db()
    await service.rebuild_index(posts_dir)
    drafts = await service.get_posts(status="draft")
    assert len(drafts) == 1
    assert drafts[0]["status"] == "draft"


@pytest.mark.asyncio
async def test_get_post_count(posts_dir):
    await database.init_db()
    await service.rebuild_index(posts_dir)
    count = await service.get_post_count()
    assert count == 2


@pytest.mark.asyncio
async def test_update_post_status(posts_dir):
    await database.init_db()
    await service.rebuild_index(posts_dir)
    posts = await service.get_posts()
    post_id = posts[0]["id"]
    await service.update_post_status(post_id, "approved")
    updated = await service.get_post_by_id(post_id)
    assert updated["status"] == "approved"


@pytest.mark.asyncio
async def test_extract_title_from_body(posts_dir):
    await database.init_db()
    await service.rebuild_index(posts_dir)
    posts = await service.get_posts()
    titles = [p["title"] for p in posts]
    assert "Breaking: AI news today" in titles
    assert "This has no front matter" in titles
