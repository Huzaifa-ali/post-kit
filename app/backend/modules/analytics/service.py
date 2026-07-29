"""Analytics service — CSV/Excel import, aggregation, export."""

import csv
import io
import json
from datetime import datetime
from pathlib import Path

from backend.config import APP_DIR
from backend.core.database import get_db

IMPORTS_DIR = APP_DIR / "data" / "imports"


def _ensure_imports_dir() -> None:
    """Ensure imports backup directory exists."""
    IMPORTS_DIR.mkdir(parents=True, exist_ok=True)


async def import_csv(filename: str, content: bytes) -> dict:
    """Import CSV data into analytics table. Returns summary."""
    _ensure_imports_dir()
    backup_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
    (IMPORTS_DIR / backup_name).write_bytes(content)

    text = content.decode("utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    columns = reader.fieldnames or []
    rows = list(reader)

    db = await get_db()
    try:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                import_file TEXT NOT NULL,
                imported_at TEXT NOT NULL,
                data_json TEXT NOT NULL
            )"""
        )
        await db.execute(
            "INSERT INTO analytics (import_file, imported_at, data_json) VALUES (?, ?, ?)",
            (backup_name, datetime.now().isoformat(), json.dumps(rows)),
        )
        await db.commit()
    finally:
        await db.close()

    return {"rows_imported": len(rows), "columns": list(columns), "filename": backup_name}


async def get_dashboard_data() -> dict:
    """Get aggregated analytics data for dashboard."""
    db = await get_db()
    try:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                import_file TEXT NOT NULL,
                imported_at TEXT NOT NULL,
                data_json TEXT NOT NULL
            )"""
        )
        cursor = await db.execute(
            "SELECT * FROM analytics ORDER BY imported_at DESC LIMIT 10"
        )
        rows = await cursor.fetchall()
    finally:
        await db.close()

    all_data: list[dict] = []
    columns: set[str] = set()
    for row in rows:
        data = json.loads(row["data_json"])
        all_data.extend(data)
        for item in data:
            columns.update(item.keys())

    return {
        "total_posts": len(all_data),
        "columns": sorted(columns),
        "data": all_data[:100],
    }


async def export_data() -> list[dict]:
    """Export all analytics data as a list of dicts."""
    db = await get_db()
    try:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                import_file TEXT NOT NULL,
                imported_at TEXT NOT NULL,
                data_json TEXT NOT NULL
            )"""
        )
        cursor = await db.execute("SELECT data_json FROM analytics ORDER BY imported_at DESC")
        rows = await cursor.fetchall()
    finally:
        await db.close()

    all_data: list[dict] = []
    for row in rows:
        all_data.extend(json.loads(row["data_json"]))
    return all_data
