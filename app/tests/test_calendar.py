"""Tests for the calendar module."""

import pytest
from pathlib import Path

from backend.core import database
from backend.modules.calendar import service
from backend.modules.library import service as library_service


@pytest.fixture(autouse=True)
def use_temp_db(tmp_path, monkeypatch):
    test_db = tmp_path / "test.db"
    monkeypatch.setattr(database, "DB_PATH", test_db)


@pytest.fixture
def posts_dir(tmp_path) -> Path:
    month_dir = tmp_path / "posts" / "2026-july"
    month_dir.mkdir(parents=True)
    (month_dir / "post-one.md").write_text(
        "---\nstatus: approved\n---\nFirst post",
        encoding="utf-8",
    )
    (month_dir / "post-two.md").write_text(
        "---\nstatus: published\ncreated: 2026-07-20T14:00:00\n---\nSecond post",
        encoding="utf-8",
    )
    return tmp_path / "posts"


@pytest.mark.asyncio
async def test_build_calendar_days_correct_count():
    posts = []
    cadence = {"best_days": ["tuesday"], "slow_days": ["monday"]}
    days = service.build_calendar_days(2026, 7, posts, cadence)
    assert len(days) == 31


@pytest.mark.asyncio
async def test_build_calendar_days_with_cadence():
    cadence = {"best_days": ["tuesday"], "slow_days": ["sunday"]}
    days = service.build_calendar_days(2026, 7, [], cadence)
    tuesdays = [d for d in days if d["is_best_day"]]
    sundays = [d for d in days if d["is_slow_day"]]
    assert len(tuesdays) > 0
    assert len(sundays) > 0


@pytest.mark.asyncio
async def test_get_queue_empty():
    await database.init_db()
    queue = await service.get_queue()
    assert queue == []


@pytest.mark.asyncio
async def test_get_month_posts(posts_dir):
    await database.init_db()
    await library_service.rebuild_index(posts_dir)
    posts = await service.get_month_posts(2026, 7)
    assert len(posts) >= 1
