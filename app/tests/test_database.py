"""Tests for SQLite database module."""

import pytest
from pathlib import Path

from backend.core import database


@pytest.fixture(autouse=True)
def use_temp_db(tmp_path, monkeypatch):
    """Use a temporary database for each test."""
    test_db = tmp_path / "test.db"
    monkeypatch.setattr(database, "DB_PATH", test_db)


@pytest.mark.asyncio
async def test_init_creates_tables():
    await database.init_db()
    db = await database.get_db()
    try:
        cursor = await db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [row["name"] for row in await cursor.fetchall()]
    finally:
        await db.close()
    assert "posts" in tables
    assert "notifications" in tables
    assert "meta" in tables


@pytest.mark.asyncio
async def test_last_index_time_none_initially():
    await database.init_db()
    result = await database.get_last_index_time()
    assert result is None


@pytest.mark.asyncio
async def test_set_and_get_last_index_time():
    await database.init_db()
    await database.set_last_index_time()
    result = await database.get_last_index_time()
    assert result is not None


@pytest.mark.asyncio
async def test_is_index_stale_when_no_build():
    await database.init_db()
    assert await database.is_index_stale(Path("/nonexistent")) is True


@pytest.mark.asyncio
async def test_is_index_stale_with_no_posts_dir():
    await database.init_db()
    await database.set_last_index_time()
    assert await database.is_index_stale(Path("/nonexistent")) is False
