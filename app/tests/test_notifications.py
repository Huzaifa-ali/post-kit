"""Tests for notifications module."""

import pytest
from backend.core import database
from backend.modules.notifications import service


@pytest.fixture(autouse=True)
def use_temp_db(tmp_path, monkeypatch):
    test_db = tmp_path / "test.db"
    monkeypatch.setattr(database, "DB_PATH", test_db)


@pytest.mark.asyncio
async def test_create_notification():
    await database.init_db()
    nid = await service.create_notification("test", "Hello world", "/library")
    assert nid is not None
    assert nid > 0


@pytest.mark.asyncio
async def test_get_notifications():
    await database.init_db()
    await service.create_notification("info", "First")
    await service.create_notification("info", "Second")
    notifs = await service.get_notifications()
    assert len(notifs) == 2


@pytest.mark.asyncio
async def test_unread_count():
    await database.init_db()
    await service.create_notification("info", "Unread one")
    count = await service.get_unread_count()
    assert count == 1


@pytest.mark.asyncio
async def test_mark_as_read():
    await database.init_db()
    nid = await service.create_notification("info", "Read me")
    await service.mark_as_read(nid)
    count = await service.get_unread_count()
    assert count == 0
