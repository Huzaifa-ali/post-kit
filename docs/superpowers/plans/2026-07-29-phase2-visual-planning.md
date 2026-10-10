# Post-Kit Desktop UI — Phase 2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Calendar (queue + scheduling), Images (MCP generation + media library), and Brand (niche file editing) modules to the app.

**Architecture:** Same as Phase 1 — modular FastAPI backend, Jinja2 templates, vanilla JS. Each new module follows the router/service/models pattern. No changes to existing modules.

**Tech Stack:** Same as Phase 1. New additions: MCP client (stdlib subprocess/asyncio), drag-and-drop (vanilla JS).

**Spec:** `docs/superpowers/specs/2026-07-29-post-kit-ui-design.md`
**Depends on:** Phase 1 complete (Tasks 1-9)

---

## File Structure (Phase 2 additions)

```
app/
├── backend/
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── client.py          # MCP client (spawn + communicate)
│   │   └── registry.py        # Discover MCP servers from config
│   ├── modules/
│   │   ├── calendar/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── service.py
│   │   │   └── router.py
│   │   ├── images/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── service.py
│   │   │   └── router.py
│   │   └── brand/
│   │       ├── __init__.py
│   │       ├── service.py
│   │       └── router.py
├── frontend/
│   ├── templates/
│   │   ├── calendar.html
│   │   ├── images.html
│   │   └── brand.html
│   ├── static/js/
│   │   ├── calendar.js
│   │   └── editor.js
│   └── data/
│       └── media/             # Image storage directory
```



---

## Task 1: Calendar Module — Backend

**Files:**
- Create: `app/backend/modules/calendar/__init__.py`
- Create: `app/backend/modules/calendar/models.py`
- Create: `app/backend/modules/calendar/service.py`
- Create: `app/backend/modules/calendar/router.py`
- Create: `app/tests/test_calendar.py`
- Modify: `app/backend/main.py` (mount router)

- [ ] **Step 1: Create calendar/models.py**

```python
"""Calendar module data models."""

from pydantic import BaseModel


class CalendarDay(BaseModel):
    """A single day in the calendar view."""
    date: str
    posts: list[dict]
    is_best_day: bool = False
    is_slow_day: bool = False


class CalendarMonth(BaseModel):
    """Full month of calendar data."""
    year: int
    month: int
    days: list[CalendarDay]
    cadence: dict | None = None


class SchedulePostRequest(BaseModel):
    """Request to schedule a post to a date."""
    scheduled_date: str
```

- [ ] **Step 2: Create calendar/service.py**

```python
"""Calendar service — scheduling and cadence logic."""

from datetime import date, datetime, timedelta
from calendar import monthrange

from backend.core.database import get_db
from backend.core.bridge import PostKitBridge


async def get_month_posts(year: int, month: int) -> list[dict]:
    """Get all posts for a given month from the index."""
    month_start = f"{year}-{month:02d}-01"
    month_end = f"{year}-{month:02d}-{monthrange(year, month)[1]}"
    db = await get_db()
    try:
        cursor = await db.execute(
            """SELECT * FROM posts
               WHERE created_at >= ? AND created_at <= ?
               ORDER BY created_at ASC""",
            (month_start, month_end + "T23:59:59"),
        )
        rows = await cursor.fetchall()
    finally:
        await db.close()
    return [dict(row) for row in rows]


def build_calendar_days(
    year: int, month: int, posts: list[dict], cadence: dict | None
) -> list[dict]:
    """Build calendar day objects with posts mapped and cadence overlay."""
    num_days = monthrange(year, month)[1]
    best_days = cadence.get("best_days", []) if cadence else []
    slow_days = cadence.get("slow_days", []) if cadence else []

    days = []
    for day_num in range(1, num_days + 1):
        current_date = date(year, month, day_num)
        day_name = current_date.strftime("%A").lower()
        date_str = current_date.isoformat()

        day_posts = [p for p in posts if p.get("created_at", "").startswith(date_str)]

        days.append({
            "date": date_str,
            "posts": day_posts,
            "is_best_day": day_name in best_days,
            "is_slow_day": day_name in slow_days,
            "day_name": day_name,
            "day_number": day_num,
        })
    return days


async def schedule_post(post_id: str, scheduled_date: str) -> None:
    """Assign a scheduled date to a post."""
    db = await get_db()
    try:
        await db.execute(
            "UPDATE posts SET created_at = ?, updated_at = ? WHERE id = ?",
            (scheduled_date, datetime.now().isoformat(), post_id),
        )
        await db.commit()
    finally:
        await db.close()


async def get_queue() -> list[dict]:
    """Get approved posts not yet published (the queue)."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT * FROM posts WHERE status = 'approved' ORDER BY created_at ASC"
        )
        rows = await cursor.fetchall()
    finally:
        await db.close()
    return [dict(row) for row in rows]
```

- [ ] **Step 3: Create calendar/router.py**

```python
"""Calendar module routes — month view and scheduling."""

from fastapi import APIRouter, HTTPException

from backend.modules.calendar import service
from backend.modules.calendar.models import CalendarMonth, SchedulePostRequest

router = APIRouter(prefix="/api/calendar", tags=["calendar"])


@router.get("/month/{year}/{month}")
async def get_month(year: int, month: int) -> dict:
    """Get calendar data for a month."""
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Invalid month")
    posts = await service.get_month_posts(year, month)
    days = service.build_calendar_days(year, month, posts, None)
    return {"year": year, "month": month, "days": days}


@router.get("/queue")
async def get_queue() -> list[dict]:
    """Get the post queue (approved, not yet published)."""
    return await service.get_queue()


@router.put("/schedule/{post_id}")
async def schedule_post(post_id: str, request: SchedulePostRequest) -> dict[str, str]:
    """Schedule a post to a specific date."""
    await service.schedule_post(post_id, request.scheduled_date)
    return {"status": "scheduled"}
```

- [ ] **Step 4: Write tests**

```python
"""Tests for the calendar module."""

import pytest
from datetime import date

from backend.core import database
from backend.modules.calendar import service
from backend.modules.library import service as library_service


@pytest.fixture(autouse=True)
def use_temp_db(tmp_path, monkeypatch):
    test_db = tmp_path / "test.db"
    monkeypatch.setattr(database, "DB_PATH", test_db)


@pytest.fixture
def posts_dir(tmp_path) -> "Path":
    from pathlib import Path
    month_dir = tmp_path / "posts" / "2026-july"
    month_dir.mkdir(parents=True)
    (month_dir / "post-one.md").write_text(
        "---\nstatus: approved\ncreated: 2026-07-15T10:00:00\n---\nFirst post",
        encoding="utf-8",
    )
    (month_dir / "post-two.md").write_text(
        "---\nstatus: published\ncreated: 2026-07-20T14:00:00\n---\nSecond post",
        encoding="utf-8",
    )
    return tmp_path / "posts"


@pytest.mark.asyncio
async def test_get_month_posts(posts_dir):
    await database.init_db()
    await library_service.rebuild_index(posts_dir)
    posts = await service.get_month_posts(2026, 7)
    assert len(posts) == 2


@pytest.mark.asyncio
async def test_build_calendar_days():
    posts = [{"created_at": "2026-07-15T10:00:00", "title": "Test"}]
    cadence = {"best_days": ["tuesday", "wednesday"], "slow_days": ["monday"]}
    days = service.build_calendar_days(2026, 7, posts, cadence)
    assert len(days) == 31
    day_15 = days[14]
    assert len(day_15["posts"]) == 1


@pytest.mark.asyncio
async def test_get_queue_empty():
    await database.init_db()
    queue = await service.get_queue()
    assert queue == []
```

- [ ] **Step 5: Mount router in main.py**

Add import and `app.include_router(calendar_router)` to `app/backend/main.py`.

- [ ] **Step 6: Run tests, commit**

```
python -m pytest tests/test_calendar.py -v
git add app/backend/modules/calendar/ app/tests/test_calendar.py app/backend/main.py
git commit -m "feat: add calendar module with month view and queue"
```



---

## Task 2: Images Module — Media Library & Upload

**Files:**
- Create: `app/backend/modules/images/__init__.py`
- Create: `app/backend/modules/images/models.py`
- Create: `app/backend/modules/images/service.py`
- Create: `app/backend/modules/images/router.py`
- Create: `app/data/media/.gitkeep`
- Create: `app/tests/test_images.py`
- Modify: `app/backend/main.py` (mount router)

- [ ] **Step 1: Create images/models.py**

```python
"""Images module data models."""

from pydantic import BaseModel, Field


class ImageMetadata(BaseModel):
    """Metadata for a stored image."""
    filename: str
    created_at: str
    tags: list[str] = []
    associated_post: str | None = None
    size_bytes: int = 0


class UploadResponse(BaseModel):
    """Response after uploading an image."""
    filename: str
    path: str


class GenerateImageRequest(BaseModel):
    """Request to generate an image via MCP."""
    prompt: str = Field(min_length=1, max_length=2000)
    post_id: str | None = None
```

- [ ] **Step 2: Create images/service.py**

```python
"""Images service — media library and file management."""

import json
import shutil
from datetime import datetime
from pathlib import Path

from backend.config import APP_DIR

MEDIA_DIR = APP_DIR / "data" / "media"
MANIFEST_PATH = MEDIA_DIR / "manifest.json"


def _ensure_media_dir() -> None:
    """Ensure media directory exists."""
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)


def _load_manifest() -> list[dict]:
    """Load the image manifest."""
    if not MANIFEST_PATH.exists():
        return []
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _save_manifest(manifest: list[dict]) -> None:
    """Save the image manifest."""
    _ensure_media_dir()
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def list_images(tag: str | None = None) -> list[dict]:
    """List all images in media library, optionally filtered by tag."""
    manifest = _load_manifest()
    if tag:
        return [img for img in manifest if tag in img.get("tags", [])]
    return manifest


def save_uploaded_image(filename: str, content: bytes, tags: list[str] | None = None) -> dict:
    """Save an uploaded image to media directory."""
    _ensure_media_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = f"{timestamp}_{filename}"
    filepath = MEDIA_DIR / safe_name
    filepath.write_bytes(content)

    entry = {
        "filename": safe_name,
        "original_name": filename,
        "created_at": datetime.now().isoformat(),
        "tags": tags or [],
        "associated_post": None,
        "size_bytes": len(content),
    }

    manifest = _load_manifest()
    manifest.append(entry)
    _save_manifest(manifest)
    return entry


def delete_image(filename: str) -> bool:
    """Delete an image from media library."""
    filepath = MEDIA_DIR / filename
    if filepath.exists():
        filepath.unlink()
    manifest = _load_manifest()
    manifest = [img for img in manifest if img["filename"] != filename]
    _save_manifest(manifest)
    return True


def get_image_path(filename: str) -> Path | None:
    """Get full path to an image file."""
    filepath = MEDIA_DIR / filename
    return filepath if filepath.exists() else None
```

- [ ] **Step 3: Create images/router.py**

```python
"""Images module routes — media library and upload."""

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse

from backend.modules.images import service
from backend.modules.images.models import ImageMetadata, UploadResponse, GenerateImageRequest

router = APIRouter(prefix="/api/images", tags=["images"])


@router.get("/list")
async def list_images(tag: str | None = None) -> list[dict]:
    """List all images in media library."""
    return service.list_images(tag=tag)


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)) -> UploadResponse:
    """Upload an image to the media library."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(status_code=413, detail="File too large (max 10MB)")
    entry = service.save_uploaded_image(file.filename, content)
    return UploadResponse(filename=entry["filename"], path=f"/api/images/file/{entry['filename']}")


@router.get("/file/{filename}")
async def get_image_file(filename: str) -> FileResponse:
    """Serve an image file."""
    filepath = service.get_image_path(filename)
    if not filepath:
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(filepath)


@router.delete("/{filename}")
async def delete_image(filename: str) -> dict[str, str]:
    """Delete an image from the library."""
    service.delete_image(filename)
    return {"status": "deleted"}


@router.post("/generate")
async def generate_image(request: GenerateImageRequest) -> dict[str, str]:
    """Generate an image via MCP (stub — requires MCP server configured)."""
    return {
        "status": "not_configured",
        "message": "MCP image server not configured. Add one in Settings.",
    }
```

- [ ] **Step 4: Write tests**

```python
"""Tests for the images module."""

import pytest
from backend.modules.images import service


@pytest.fixture(autouse=True)
def use_temp_media(tmp_path, monkeypatch):
    media_dir = tmp_path / "media"
    media_dir.mkdir()
    monkeypatch.setattr(service, "MEDIA_DIR", media_dir)
    monkeypatch.setattr(service, "MANIFEST_PATH", media_dir / "manifest.json")


def test_list_images_empty():
    assert service.list_images() == []


def test_save_and_list_image():
    entry = service.save_uploaded_image("test.png", b"fake-image-data", tags=["hero"])
    assert entry["original_name"] == "test.png"
    assert entry["size_bytes"] == len(b"fake-image-data")
    images = service.list_images()
    assert len(images) == 1


def test_filter_by_tag():
    service.save_uploaded_image("a.png", b"data", tags=["hero"])
    service.save_uploaded_image("b.png", b"data", tags=["meme"])
    assert len(service.list_images(tag="hero")) == 1
    assert len(service.list_images(tag="meme")) == 1


def test_delete_image():
    entry = service.save_uploaded_image("del.png", b"data")
    service.delete_image(entry["filename"])
    assert service.list_images() == []
```

- [ ] **Step 5: Mount router in main.py, commit**

```
git add app/backend/modules/images/ app/data/media/.gitkeep app/tests/test_images.py app/backend/main.py
git commit -m "feat: add images module with media library and upload"
```



---

## Task 3: MCP Client — Registry & Communication

**Files:**
- Create: `app/backend/mcp/__init__.py`
- Create: `app/backend/mcp/registry.py`
- Create: `app/backend/mcp/client.py`
- Create: `app/tests/test_mcp.py`

- [ ] **Step 1: Create mcp/registry.py**

```python
"""MCP server registry — discovers available servers from config."""

from backend.config import load_config


def get_configured_servers() -> dict[str, dict]:
    """Get all configured MCP servers from app config."""
    config = load_config()
    return config.get("mcp_servers", {})


def get_image_server() -> dict | None:
    """Get the configured image generation MCP server, if any."""
    servers = get_configured_servers()
    for name, server_config in servers.items():
        if server_config.get("disabled", False):
            continue
        # Return first non-disabled server (user configures which one)
        return {"name": name, **server_config}
    return None


def has_image_server() -> bool:
    """Check if any image MCP server is configured and enabled."""
    return get_image_server() is not None
```

- [ ] **Step 2: Create mcp/client.py**

```python
"""MCP client — spawns and communicates with MCP servers via stdio."""

import asyncio
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class MCPClient:
    """Client that spawns an MCP server process and communicates via stdio JSON-RPC."""

    def __init__(self, command: str, args: list[str], env: dict | None = None):
        self._command = command
        self._args = args
        self._env = env
        self._process: asyncio.subprocess.Process | None = None

    async def connect(self) -> bool:
        """Spawn the MCP server process."""
        try:
            self._process = await asyncio.create_subprocess_exec(
                self._command, *self._args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            logger.info(f"MCP server started: {self._command}")
            return True
        except FileNotFoundError:
            logger.error(f"MCP server not found: {self._command}")
            return False

    async def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """Call a tool on the MCP server via JSON-RPC."""
        if not self._process or not self._process.stdin or not self._process.stdout:
            return {"error": "MCP server not connected"}

        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
            "id": 1,
        }

        self._process.stdin.write(json.dumps(request).encode() + b"\n")
        await self._process.stdin.drain()

        try:
            line = await asyncio.wait_for(
                self._process.stdout.readline(), timeout=60.0
            )
            if line:
                return json.loads(line.decode())
            return {"error": "No response from MCP server"}
        except asyncio.TimeoutError:
            return {"error": "MCP server timed out"}

    async def disconnect(self) -> None:
        """Terminate the MCP server process."""
        if self._process and self._process.returncode is None:
            self._process.terminate()
            try:
                await asyncio.wait_for(self._process.wait(), timeout=3.0)
            except asyncio.TimeoutError:
                self._process.kill()
            logger.info("MCP server disconnected")

    @property
    def is_connected(self) -> bool:
        """Check if the server process is still running."""
        return self._process is not None and self._process.returncode is None
```

- [ ] **Step 3: Write tests**

```python
"""Tests for MCP client and registry."""

import pytest
from unittest.mock import patch, AsyncMock

from backend.mcp.registry import get_configured_servers, has_image_server
from backend.mcp.client import MCPClient


def test_no_servers_configured(monkeypatch):
    monkeypatch.setattr(
        "backend.mcp.registry.load_config",
        lambda: {"adapter": "kiro"},
    )
    assert get_configured_servers() == {}
    assert has_image_server() is False


def test_has_image_server(monkeypatch):
    monkeypatch.setattr(
        "backend.mcp.registry.load_config",
        lambda: {"mcp_servers": {"img": {"command": "uvx", "args": [], "disabled": False}}},
    )
    assert has_image_server() is True


def test_disabled_server_not_returned(monkeypatch):
    monkeypatch.setattr(
        "backend.mcp.registry.load_config",
        lambda: {"mcp_servers": {"img": {"command": "uvx", "args": [], "disabled": True}}},
    )
    assert has_image_server() is False


@pytest.mark.asyncio
@patch("backend.mcp.client.asyncio.create_subprocess_exec", side_effect=FileNotFoundError)
async def test_mcp_client_connect_fails(mock_exec):
    client = MCPClient("nonexistent", [])
    result = await client.connect()
    assert result is False


@pytest.mark.asyncio
async def test_mcp_client_call_without_connect():
    client = MCPClient("cmd", [])
    result = await client.call_tool("test", {})
    assert "error" in result
```

- [ ] **Step 4: Commit**

```
git add app/backend/mcp/ app/tests/test_mcp.py
git commit -m "feat: add MCP client and server registry"
```



---

## Task 4: Brand Module — Niche File Editing

**Files:**
- Create: `app/backend/modules/brand/__init__.py`
- Create: `app/backend/modules/brand/service.py`
- Create: `app/backend/modules/brand/router.py`
- Create: `app/tests/test_brand.py`
- Modify: `app/backend/main.py` (mount router)

- [ ] **Step 1: Create brand/service.py**

```python
"""Brand service — niche file listing and editing via bridge."""

from backend.core.bridge import PostKitBridge


def list_niche_files(bridge: PostKitBridge) -> list[dict]:
    """List all files in my-niche/ with summary info."""
    files = bridge.list_niche_files()
    result = []
    for filename in sorted(files):
        content = bridge.read_niche_file(filename)
        first_line = ""
        if content:
            for line in content.split("\n"):
                stripped = line.strip().lstrip("#").strip()
                if stripped:
                    first_line = stripped[:80]
                    break
        result.append({
            "filename": filename,
            "summary": first_line,
            "size": len(content) if content else 0,
        })
    return result


def get_file_content(bridge: PostKitBridge, filename: str) -> str | None:
    """Get the content of a niche file."""
    return bridge.read_niche_file(filename)


def save_file_content(bridge: PostKitBridge, filename: str, content: str) -> None:
    """Save edited content to a niche file."""
    bridge.write_niche_file(filename, content)
```

- [ ] **Step 2: Create brand/router.py**

```python
"""Brand module routes — niche file listing and editing."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.config import get_postkit_root
from backend.core.bridge import PostKitBridge
from backend.modules.brand import service

router = APIRouter(prefix="/api/brand", tags=["brand"])


class SaveFileRequest(BaseModel):
    content: str


@router.get("/files")
async def list_files() -> list[dict]:
    """List all niche files."""
    bridge = PostKitBridge(get_postkit_root())
    return service.list_niche_files(bridge)


@router.get("/files/{filename}")
async def get_file(filename: str) -> dict:
    """Get content of a niche file."""
    bridge = PostKitBridge(get_postkit_root())
    content = service.get_file_content(bridge, filename)
    if content is None:
        raise HTTPException(status_code=404, detail="File not found")
    return {"filename": filename, "content": content}


@router.put("/files/{filename}")
async def save_file(filename: str, request: SaveFileRequest) -> dict[str, str]:
    """Save edited content to a niche file."""
    bridge = PostKitBridge(get_postkit_root())
    service.save_file_content(bridge, filename, request.content)
    return {"status": "saved"}
```

- [ ] **Step 3: Write tests**

```python
"""Tests for the brand module."""

import pytest
from pathlib import Path

from backend.core.bridge import PostKitBridge
from backend.modules.brand import service


@pytest.fixture
def bridge_with_files(tmp_path) -> PostKitBridge:
    niche_dir = tmp_path / "my-niche"
    niche_dir.mkdir()
    (niche_dir / "voice.md").write_text("# Voice\nBe direct and opinionated.", encoding="utf-8")
    (niche_dir / "niche.yaml").write_text("name: Test\nplatforms: [linkedin]", encoding="utf-8")
    return PostKitBridge(tmp_path)


def test_list_niche_files(bridge_with_files):
    files = service.list_niche_files(bridge_with_files)
    filenames = [f["filename"] for f in files]
    assert "voice.md" in filenames
    assert "niche.yaml" in filenames


def test_file_summary_extracted(bridge_with_files):
    files = service.list_niche_files(bridge_with_files)
    voice_file = next(f for f in files if f["filename"] == "voice.md")
    assert "Voice" in voice_file["summary"]


def test_get_file_content(bridge_with_files):
    content = service.get_file_content(bridge_with_files, "voice.md")
    assert "Be direct" in content


def test_get_nonexistent_file(bridge_with_files):
    content = service.get_file_content(bridge_with_files, "missing.md")
    assert content is None


def test_save_file_content(bridge_with_files):
    service.save_file_content(bridge_with_files, "voice.md", "# Updated Voice\nNew content.")
    content = service.get_file_content(bridge_with_files, "voice.md")
    assert "New content" in content
```

- [ ] **Step 4: Mount router in main.py, commit**

```
git add app/backend/modules/brand/ app/tests/test_brand.py app/backend/main.py
git commit -m "feat: add brand module for niche file editing"
```



---

## Task 5: Frontend — Calendar, Images, Brand Pages

**Files:**
- Create: `app/frontend/templates/calendar.html`
- Create: `app/frontend/templates/images.html`
- Create: `app/frontend/templates/brand.html`
- Create: `app/frontend/static/js/calendar.js`
- Create: `app/frontend/static/js/editor.js`
- Modify: `app/backend/main.py` (add page routes for /calendar, /images, /brand)

- [ ] **Step 1: Create calendar.html**

```html
{% extends "base.html" %}
{% block title %}Calendar — post-kit{% endblock %}
{% block page_title %}Calendar{% endblock %}

{% block content %}
<section class="flex gap-6" style="height: calc(100vh - 8rem);">
  <!-- Calendar grid -->
  <div class="flex-1 overflow-y-auto">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-lg font-semibold" data-calendar-title>{{ month_name }} {{ year }}</h2>
      <div class="flex gap-2">
        <button data-action="prev-month" class="px-3 py-1 rounded-lg border bg-surface-raised text-sm hover:bg-surface-overlay transition-colors">&larr;</button>
        <button data-action="next-month" class="px-3 py-1 rounded-lg border bg-surface-raised text-sm hover:bg-surface-overlay transition-colors">&rarr;</button>
      </div>
    </div>

    <div data-calendar-grid class="grid gap-1" style="grid-template-columns: repeat(7, 1fr);">
      <!-- Day headers -->
      <div class="text-xs text-muted text-center py-1 font-medium">Mon</div>
      <div class="text-xs text-muted text-center py-1 font-medium">Tue</div>
      <div class="text-xs text-muted text-center py-1 font-medium">Wed</div>
      <div class="text-xs text-muted text-center py-1 font-medium">Thu</div>
      <div class="text-xs text-muted text-center py-1 font-medium">Fri</div>
      <div class="text-xs text-muted text-center py-1 font-medium">Sat</div>
      <div class="text-xs text-muted text-center py-1 font-medium">Sun</div>

      <!-- Days populated by JS -->
    </div>
  </div>

  <!-- Queue sidebar -->
  <aside class="w-64 border-l overflow-y-auto p-4" style="border-color: var(--color-border);">
    <h3 class="text-sm font-semibold mb-3">Queue</h3>
    <div data-queue-list class="space-y-2">
      {% for post in queue %}
        <div class="text-xs p-2 rounded-lg bg-surface-raised border cursor-pointer" data-post-id="{{ post.id }}">
          {{ post.title }}
        </div>
      {% endfor %}
      {% if not queue %}
        <p class="text-xs text-muted">No posts in queue. Approve posts from Library.</p>
      {% endif %}
    </div>
  </aside>
</section>
{% endblock %}

{% block scripts %}
<script type="module" src="/static/js/calendar.js"></script>
{% endblock %}
```

- [ ] **Step 2: Create calendar.js**

```javascript
/** Calendar page — month grid rendering and navigation. */
import { api, $ } from './app.js';

const grid = $('[data-calendar-grid]');
const title = $('[data-calendar-title]');
let currentYear = new Date().getFullYear();
let currentMonth = new Date().getMonth() + 1;

async function loadMonth(year, month) {
  const data = await api(`/calendar/month/${year}/${month}`);
  renderDays(data.days, year, month);
  const monthName = new Date(year, month - 1).toLocaleString('default', { month: 'long' });
  if (title) title.textContent = `${monthName} ${year}`;
}

function renderDays(days, year, month) {
  if (!grid) return;
  // Clear existing day cells (keep headers)
  const headers = grid.querySelectorAll(':scope > div:nth-child(-n+7)');
  grid.innerHTML = '';
  headers.forEach(h => grid.appendChild(h));

  // Calculate starting day offset (Monday = 0)
  const firstDay = new Date(year, month - 1, 1).getDay();
  const offset = firstDay === 0 ? 6 : firstDay - 1;
  for (let i = 0; i < offset; i++) {
    grid.appendChild(createEmptyCell());
  }

  days.forEach(day => {
    const cell = document.createElement('div');
    cell.className = 'rounded-lg border p-2 text-xs';
    cell.style.minHeight = '4rem';
    cell.style.borderColor = 'var(--color-border-subtle)';

    if (day.is_best_day) cell.style.borderColor = 'var(--color-accent)';
    if (day.is_slow_day) cell.style.opacity = '0.6';

    const num = document.createElement('span');
    num.className = 'font-medium text-secondary';
    num.textContent = day.day_number;
    cell.appendChild(num);

    day.posts.forEach(post => {
      const dot = document.createElement('div');
      dot.className = 'mt-1 truncate text-xs';
      dot.style.color = `var(--color-status-${post.status})`;
      dot.textContent = post.title;
      cell.appendChild(dot);
    });

    grid.appendChild(cell);
  });
}

function createEmptyCell() {
  const cell = document.createElement('div');
  cell.style.minHeight = '4rem';
  return cell;
}

// Navigation
$('[data-action="prev-month"]')?.addEventListener('click', () => {
  currentMonth--;
  if (currentMonth < 1) { currentMonth = 12; currentYear--; }
  loadMonth(currentYear, currentMonth);
});

$('[data-action="next-month"]')?.addEventListener('click', () => {
  currentMonth++;
  if (currentMonth > 12) { currentMonth = 1; currentYear++; }
  loadMonth(currentYear, currentMonth);
});

// Initial load
if (grid) loadMonth(currentYear, currentMonth);
```

- [ ] **Step 3: Create images.html**

```html
{% extends "base.html" %}
{% block title %}Images — post-kit{% endblock %}
{% block page_title %}Images{% endblock %}

{% block content %}
<section class="space-y-6">
  <!-- Tabs -->
  <div class="flex gap-1 border-b">
    <button data-tab="library" class="px-4 py-2 text-sm font-medium" style="border-bottom: 2px solid var(--color-accent); color: var(--color-text-primary);">Library</button>
    <button data-tab="upload" class="px-4 py-2 text-sm font-medium text-secondary" style="border-bottom: 2px solid transparent;">Upload</button>
    <button data-tab="generate" class="px-4 py-2 text-sm font-medium text-secondary" style="border-bottom: 2px solid transparent;">Generate</button>
  </div>

  <!-- Library view -->
  <div data-view="library">
    <div data-image-grid class="grid gap-4" style="grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));">
      {% for image in images %}
        <div class="rounded-lg border overflow-hidden cursor-pointer hover:border-accent/50 transition-colors">
          <img src="/api/images/file/{{ image.filename }}" alt="{{ image.original_name }}"
               class="w-full" style="aspect-ratio: 1; object-fit: cover;">
          <div class="p-2">
            <p class="text-xs text-secondary truncate">{{ image.original_name }}</p>
          </div>
        </div>
      {% endfor %}
      {% if not images %}
        <p class="text-secondary" style="grid-column: 1 / -1; text-align: center; padding: 3rem 0;">
          No images yet. Upload or generate your first one.
        </p>
      {% endif %}
    </div>
  </div>

  <!-- Upload view (hidden by default) -->
  <div data-view="upload" class="hidden">
    <form data-upload-form class="border rounded-xl p-8 border-dashed" style="border-color: var(--color-border); text-align: center;">
      <p class="text-secondary mb-4">Drag and drop an image or click to browse</p>
      <input type="file" data-file-input accept="image/*" class="hidden">
      <button type="button" data-action="browse" class="px-4 py-2 rounded-lg bg-accent text-white text-sm font-medium hover:bg-accent-hover transition-colors">
        Choose File
      </button>
    </form>
  </div>

  <!-- Generate view (hidden by default) -->
  <div data-view="generate" class="hidden">
    <form data-generate-form class="space-y-4">
      <textarea data-prompt-input placeholder="Describe the image you want to generate..."
                class="w-full px-4 py-3 rounded-xl border bg-surface-raised text-primary text-sm"
                style="outline: none; min-height: 6rem; resize: vertical;"></textarea>
      <button type="submit" class="px-4 py-2 rounded-lg bg-accent text-white text-sm font-medium hover:bg-accent-hover transition-colors">
        Generate
      </button>
      {% if not mcp_available %}
        <p class="text-xs text-muted">MCP image server not configured. Add one in Settings.</p>
      {% endif %}
    </form>
  </div>
</section>
{% endblock %}
```

- [ ] **Step 4: Create brand.html**

```html
{% extends "base.html" %}
{% block title %}Brand — post-kit{% endblock %}
{% block page_title %}Brand{% endblock %}

{% block content %}
<section class="space-y-6">
  <p class="text-secondary text-sm">Your niche identity files. Edit directly or use AI to improve.</p>

  <div class="space-y-3">
    {% for file in niche_files %}
      <div class="rounded-lg border p-4 bg-surface-raised" data-file="{{ file.filename }}">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-sm font-medium text-primary">{{ file.filename }}</h3>
            <p class="text-xs text-muted mt-0.5">{{ file.summary }}</p>
          </div>
          <div class="flex gap-2">
            <button data-action="edit-file" data-filename="{{ file.filename }}"
                    class="px-3 py-1 rounded-lg border text-xs text-secondary hover:text-primary hover:bg-surface-overlay transition-colors">
              Edit
            </button>
          </div>
        </div>
      </div>
    {% endfor %}

    {% if not niche_files %}
      <p class="text-secondary text-center py-8">No niche files found. Run onboarding first.</p>
    {% endif %}
  </div>

  <!-- Editor modal (hidden, shown by JS) -->
  <div data-editor-modal class="hidden fixed inset-0 z-50 flex items-center justify-center">
    <div class="absolute inset-0" style="background: rgba(0,0,0,0.5)" data-action="close-editor"></div>
    <div class="relative w-full max-w-3xl bg-surface-raised border rounded-xl overflow-hidden" style="max-height: 80vh; box-shadow: var(--shadow-overlay);">
      <div class="flex items-center justify-between p-4 border-b">
        <h3 class="text-sm font-semibold" data-editor-filename></h3>
        <button data-action="save-file" class="px-3 py-1 rounded-lg bg-accent text-white text-xs font-medium hover:bg-accent-hover transition-colors">
          Save
        </button>
      </div>
      <textarea data-editor-content class="w-full p-4 bg-surface text-primary text-sm font-mono"
                style="outline: none; min-height: 50vh; resize: none;"></textarea>
    </div>
  </div>
</section>
{% endblock %}

{% block scripts %}
<script type="module" src="/static/js/editor.js"></script>
{% endblock %}
```

- [ ] **Step 5: Create editor.js**

```javascript
/** Editor — file editing modal for Brand page. */
import { api, $ } from './app.js';

const modal = $('[data-editor-modal]');
const filenameEl = $('[data-editor-filename]');
const contentEl = $('[data-editor-content]');
let currentFilename = null;

// Open editor on "Edit" button click
document.addEventListener('click', async (e) => {
  const btn = e.target.closest('[data-action="edit-file"]');
  if (!btn) return;

  currentFilename = btn.dataset.filename;
  const data = await api(`/brand/files/${currentFilename}`);

  if (filenameEl) filenameEl.textContent = currentFilename;
  if (contentEl) contentEl.value = data.content;
  if (modal) modal.classList.remove('hidden');
});

// Save file
$('[data-action="save-file"]')?.addEventListener('click', async () => {
  if (!currentFilename || !contentEl) return;
  await api(`/brand/files/${currentFilename}`, {
    method: 'PUT',
    body: JSON.stringify({ content: contentEl.value }),
  });
  if (modal) modal.classList.add('hidden');
  window.location.reload();
});

// Close modal
$('[data-action="close-editor"]')?.addEventListener('click', () => {
  if (modal) modal.classList.add('hidden');
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && modal && !modal.classList.contains('hidden')) {
    modal.classList.add('hidden');
  }
});
```

- [ ] **Step 6: Add page routes to main.py**

Add to `app/backend/main.py`:
```python
from backend.modules.calendar.router import router as calendar_router
from backend.modules.images.router import router as images_router
from backend.modules.brand.router import router as brand_router
from backend.modules.calendar import service as calendar_service
from backend.modules.images import service as images_service
from backend.modules.brand import service as brand_service
from backend.mcp.registry import has_image_server

app.include_router(calendar_router)
app.include_router(images_router)
app.include_router(brand_router)


@app.get("/calendar")
async def calendar_page(request: Request):
    bridge = PostKitBridge(get_postkit_root())
    queue = await calendar_service.get_queue()
    now = datetime.now()
    month_name = now.strftime("%B")
    context = {
        "queue": queue,
        "year": now.year,
        "month_name": month_name,
        **_page_context(bridge, "calendar"),
    }
    return templates.TemplateResponse(request, "calendar.html", context)


@app.get("/images")
async def images_page(request: Request):
    bridge = PostKitBridge(get_postkit_root())
    images = images_service.list_images()
    context = {
        "images": images,
        "mcp_available": has_image_server(),
        **_page_context(bridge, "images"),
    }
    return templates.TemplateResponse(request, "images.html", context)


@app.get("/brand")
async def brand_page(request: Request):
    bridge = PostKitBridge(get_postkit_root())
    niche_files = brand_service.list_niche_files(bridge)
    context = {
        "niche_files": niche_files,
        **_page_context(bridge, "brand"),
    }
    return templates.TemplateResponse(request, "brand.html", context)
```

Also update `_get_nav_context` to always include Calendar and Brand:
```python
def _get_nav_context(bridge: PostKitBridge) -> list[dict]:
    groups = [
        {"label": "Create", "items": [
            {"id": "content", "label": "Content", "icon": "✦", "url": "/content"},
        ]},
        {"label": "Manage", "items": [
            {"id": "library", "label": "Library", "icon": "📚", "url": "/library"},
            {"id": "calendar", "label": "Calendar", "icon": "📅", "url": "/calendar"},
        ]},
        {"label": "Settings", "items": [
            {"id": "brand", "label": "Brand", "icon": "🎨", "url": "/brand"},
            {"id": "settings", "label": "Settings", "icon": "⚙", "url": "/settings"},
        ]},
    ]
    modules = bridge.get_active_modules()
    if any(m in modules for m in ["visual-system", "image-prompts"]):
        groups[0]["items"].append(
            {"id": "images", "label": "Images", "icon": "🖼", "url": "/images"}
        )
    if "analytics" in modules:
        groups.insert(2, {"label": "Insights", "items": [
            {"id": "analytics", "label": "Analytics", "icon": "📊", "url": "/analytics"},
        ]})
    return groups
```

- [ ] **Step 7: Add `from datetime import datetime` import to main.py if not present**

- [ ] **Step 8: Run all tests, verify pages render, commit**

```
python -m pytest tests/ -v
git add app/frontend/ app/backend/main.py
git commit -m "feat: add calendar images and brand page templates"
```

---

## End of Phase 2 Plan

**What Phase 2 delivers:**
- Calendar module (month view, queue, scheduling, cadence overlay)
- Images module (upload, media library, manifest, generate stub via MCP)
- MCP client + registry (server discovery, stdio communication, tool calling)
- Brand module (list niche files, edit content, save via bridge)
- Three new page templates with full interactivity (calendar.js, editor.js)
- Dynamic sidebar now shows Calendar, Brand always + Images conditionally

**What comes in Phase 3:** Analytics (CSV import, dashboard, charts, export), Credits (plan display, usage tracking), Notifications (activity feed, alerts), Settings page (full config management).
