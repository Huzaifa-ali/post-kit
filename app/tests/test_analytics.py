"""Tests for the analytics module."""

import pytest
from backend.core import database
from backend.modules.analytics import service


@pytest.fixture(autouse=True)
def use_temp(tmp_path, monkeypatch):
    test_db = tmp_path / "test.db"
    monkeypatch.setattr(database, "DB_PATH", test_db)
    monkeypatch.setattr(service, "IMPORTS_DIR", tmp_path / "imports")


@pytest.mark.asyncio
async def test_import_csv():
    await database.init_db()
    csv_content = b"date,impressions,likes\n2026-07-01,1000,50\n2026-07-02,1200,65"
    result = await service.import_csv("test.csv", csv_content)
    assert result["rows_imported"] == 2
    assert "date" in result["columns"]
    assert "impressions" in result["columns"]


@pytest.mark.asyncio
async def test_dashboard_data_empty():
    await database.init_db()
    data = await service.get_dashboard_data()
    assert data["total_posts"] == 0
    assert data["data"] == []


@pytest.mark.asyncio
async def test_dashboard_after_import():
    await database.init_db()
    csv_content = b"date,views\n2026-07-01,500"
    await service.import_csv("test.csv", csv_content)
    data = await service.get_dashboard_data()
    assert data["total_posts"] == 1


@pytest.mark.asyncio
async def test_export_data():
    await database.init_db()
    csv_content = b"metric,value\nviews,1000"
    await service.import_csv("test.csv", csv_content)
    exported = await service.export_data()
    assert len(exported) == 1
    assert exported[0]["metric"] == "views"
