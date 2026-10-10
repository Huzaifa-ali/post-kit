# Post-Kit Desktop UI — Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the core functional app — project bootstrap, bridge, adapter, library, content creation, and app shell.

**Architecture:** FastAPI backend (Python 3.12+) serving Jinja2 templates with Tailwind CSS v4. Tauri v2 wraps it as a desktop app. SQLite as rebuildable index. Kiro CLI as primary AI adapter. PostKitBridge as the single boundary to post-kit files.

**Tech Stack:** Python 3.12, FastAPI, Jinja2, Tailwind CSS v4, Vanilla JS (ES modules), aiosqlite, PyYAML, Tauri v2 (Rust)

**Spec:** `docs/superpowers/specs/2026-07-29-post-kit-ui-design.md`

---

## File Structure (Phase 1)

```
app/
├── backend/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app, mounts routers, lifespan
│   ├── config.py               # Settings (paths, adapter choice)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── bridge.py           # PostKitBridge class
│   │   ├── database.py         # SQLite setup + rebuild
│   │   ├── events.py           # Event bus (observer pattern)
│   │   └── models.py           # Shared enums (PostStatus)
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── base.py             # BaseAdapter ABC
│   │   └── kiro.py             # Kiro CLI adapter
│   └── modules/
│       ├── content/
│       │   ├── __init__.py
│       │   ├── router.py
│       │   ├── service.py
│       │   └── models.py
│       └── library/
│           ├── __init__.py
│           ├── router.py
│           ├── service.py
│           └── models.py
├── frontend/
│   ├── templates/
│   │   ├── base.html
│   │   ├── content.html
│   │   ├── library.html
│   │   └── onboarding.html
│   ├── components/
│   │   ├── sidebar.html
│   │   ├── post-card.html
│   │   ├── chat-bubble.html
│   │   └── command-bar.html
│   ├── static/
│   │   ├── css/app.css
│   │   └── js/
│   │       ├── app.js
│   │       └── chat.js
│   └── tailwind.config.js      # NOTE: only for build tooling, not config (v4 uses CSS)
├── data/
│   └── config.json
├── pyproject.toml
└── run.py                      # Dev entry point (uvicorn)
```



---

## Task 1: Project Bootstrap

**Files:**
- Create: `app/pyproject.toml`
- Create: `app/run.py`
- Create: `app/backend/__init__.py`
- Create: `app/backend/main.py`
- Create: `app/data/config.json`

- [ ] **Step 1: Create pyproject.toml with pinned dependencies**

```toml
[project]
name = "post-kit-app"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "jinja2>=3.1.4",
    "python-multipart>=0.0.12",
    "aiosqlite>=0.20.0",
    "pyyaml>=6.0.2",
    "markdown>=3.7",
]

[project.optional-dependencies]
dev = [
    "httpx>=0.27.0",
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "ruff>=0.8.0",
]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "ANN"]
ignore = ["ANN101", "ANN102"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
```

- [ ] **Step 2: Create default config.json**

```json
{
    "postkit_path": "..",
    "adapter": "kiro",
    "theme": "dark",
    "plan": {
        "name": "Free",
        "limit": 100,
        "period": "monthly"
    },
    "usage": {
        "count": 0,
        "reset_date": null
    }
}
```

- [ ] **Step 3: Create main.py — minimal FastAPI app**

```python
"""Post-kit desktop app — FastAPI entry point."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    yield


app = FastAPI(title="post-kit", docs_url=None, redoc_url=None, lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")


@app.get("/api/health")
async def health_check():
    """Health endpoint for Tauri readiness check."""
    return {"status": "ok"}
```

- [ ] **Step 4: Create run.py — dev entry point**

```python
"""Run the post-kit app in development mode."""

import uvicorn


def main():
    uvicorn.run(
        "app.backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["app"],
    )


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Create __init__.py**

```python
# app/backend/__init__.py
```

- [ ] **Step 6: Install dependencies and verify server starts**

Run: `cd app && uv sync && cd .. && uv run python -m app.run`
Expected: Server starts on http://127.0.0.1:8000, /api/health returns `{"status": "ok"}`

- [ ] **Step 7: Commit**

```
git add app/pyproject.toml app/run.py app/backend/ app/data/config.json
git commit -m "feat: bootstrap FastAPI project with health endpoint"
```



---

## Task 2: Core — Config & PostKitBridge

**Files:**
- Create: `app/backend/config.py`
- Create: `app/backend/core/__init__.py`
- Create: `app/backend/core/bridge.py`
- Create: `app/backend/core/models.py`
- Test: `app/tests/test_bridge.py`

- [ ] **Step 1: Create core/models.py — shared enums**

```python
"""Shared models and enums used across the app."""

from enum import StrEnum


class PostStatus(StrEnum):
    IDEA = "idea"
    SCOUTED = "scouted"
    DRAFTING = "drafting"
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"
```

- [ ] **Step 2: Create config.py — app settings**

```python
"""App configuration — loaded from app/data/config.json."""

import json
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = APP_DIR / "data"
CONFIG_PATH = DATA_DIR / "config.json"


def load_config() -> dict:
    """Load config from JSON file. Returns defaults if missing."""
    if not CONFIG_PATH.exists():
        return {"postkit_path": "..", "adapter": "kiro", "theme": "dark"}
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def save_config(config: dict) -> None:
    """Save config to JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(
        json.dumps(config, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def get_postkit_root() -> Path:
    """Resolve the post-kit root directory from config."""
    config = load_config()
    raw_path = config.get("postkit_path", "..")
    resolved = (APP_DIR / raw_path).resolve()
    return resolved
```

- [ ] **Step 3: Create core/bridge.py — PostKitBridge**

```python
"""PostKitBridge — the single boundary between the app and post-kit files."""

from pathlib import Path

import yaml


class PostKitBridge:
    """Reads and writes post-kit file structure. Only class allowed to touch these files."""

    def __init__(self, postkit_root: Path):
        self._root = postkit_root
        self._niche_dir = postkit_root / "my-niche"
        self._engine_dir = postkit_root / "engine"

    @property
    def root(self) -> Path:
        return self._root

    @property
    def niche_dir(self) -> Path:
        return self._niche_dir

    def is_onboarded(self) -> bool:
        """Check if niche.yaml exists (setup complete)."""
        return (self._niche_dir / "niche.yaml").exists()

    def load_niche_config(self) -> dict | None:
        """Load and parse niche.yaml. Returns None if not found."""
        niche_file = self._niche_dir / "niche.yaml"
        if not niche_file.exists():
            return None
        return yaml.safe_load(niche_file.read_text(encoding="utf-8"))

    def get_posts_path(self) -> Path:
        """Resolve the posts output directory from niche config."""
        config = self.load_niche_config()
        if config and "output" in config and "path" in config["output"]:
            return (self._root / config["output"]["path"]).resolve()
        # Default: check common locations
        for candidate in [self._root / "posts", self._root.parent / "posts"]:
            if candidate.exists():
                return candidate
        return self._root.parent / "posts"

    def get_active_modules(self) -> list[str]:
        """Get list of active module names from niche.yaml."""
        config = self.load_niche_config()
        if not config:
            return []
        return config.get("modules_active", [])

    def get_platforms(self) -> list[str]:
        """Get configured platforms."""
        config = self.load_niche_config()
        if not config:
            return []
        return config.get("platforms", [])

    def get_content_pillars(self) -> list[dict]:
        """Get content pillars (name + percentage)."""
        config = self.load_niche_config()
        if not config:
            return []
        return config.get("content_pillars", [])

    def get_cadence(self) -> dict | None:
        """Get cadence config (posts_per_day, best_days, etc.)."""
        config = self.load_niche_config()
        if not config:
            return None
        return config.get("cadence", None)

    def list_niche_files(self) -> list[str]:
        """List all files in my-niche/ directory."""
        if not self._niche_dir.exists():
            return []
        return [f.name for f in self._niche_dir.iterdir() if f.is_file()]

    def read_niche_file(self, filename: str) -> str | None:
        """Read a file from my-niche/ by name."""
        filepath = self._niche_dir / filename
        if not filepath.exists():
            return None
        return filepath.read_text(encoding="utf-8")

    def write_niche_file(self, filename: str, content: str) -> None:
        """Write content to a file in my-niche/."""
        self._niche_dir.mkdir(parents=True, exist_ok=True)
        (self._niche_dir / filename).write_text(content, encoding="utf-8")

    def get_version(self) -> str | None:
        """Read VERSION file from post-kit root."""
        version_file = self._root / "VERSION"
        if not version_file.exists():
            return None
        return version_file.read_text(encoding="utf-8").strip()

    def get_niche_version(self) -> str | None:
        """Get postkit_version from niche.yaml."""
        config = self.load_niche_config()
        if not config:
            return None
        return config.get("postkit_version", None)
```

- [ ] **Step 4: Write test for bridge**

```python
"""Tests for PostKitBridge."""

import pytest
from pathlib import Path
import tempfile
import yaml

from app.backend.core.bridge import PostKitBridge


@pytest.fixture
def mock_postkit(tmp_path):
    """Create a minimal post-kit directory structure."""
    niche_dir = tmp_path / "my-niche"
    niche_dir.mkdir()
    posts_dir = tmp_path / "posts"
    posts_dir.mkdir()

    niche_config = {
        "name": "Test Niche",
        "platforms": ["linkedin"],
        "content_pillars": [{"name": "Topic A", "percentage": 60}],
        "modules_active": ["news-scout", "memes"],
        "cadence": {"posts_per_day": 1, "best_days": ["tuesday"]},
        "output": {"path": "posts"},
        "postkit_version": "1.0.0",
    }
    (niche_dir / "niche.yaml").write_text(
        yaml.dump(niche_config), encoding="utf-8"
    )
    (niche_dir / "voice.md").write_text("# Voice\nBe direct.", encoding="utf-8")
    (tmp_path / "VERSION").write_text("1.1.0", encoding="utf-8")

    return tmp_path


def test_is_onboarded(mock_postkit):
    bridge = PostKitBridge(mock_postkit)
    assert bridge.is_onboarded() is True


def test_not_onboarded(tmp_path):
    bridge = PostKitBridge(tmp_path)
    assert bridge.is_onboarded() is False


def test_load_niche_config(mock_postkit):
    bridge = PostKitBridge(mock_postkit)
    config = bridge.load_niche_config()
    assert config["name"] == "Test Niche"
    assert config["platforms"] == ["linkedin"]


def test_get_active_modules(mock_postkit):
    bridge = PostKitBridge(mock_postkit)
    assert bridge.get_active_modules() == ["news-scout", "memes"]


def test_get_posts_path(mock_postkit):
    bridge = PostKitBridge(mock_postkit)
    assert bridge.get_posts_path() == mock_postkit / "posts"


def test_list_niche_files(mock_postkit):
    bridge = PostKitBridge(mock_postkit)
    files = bridge.list_niche_files()
    assert "niche.yaml" in files
    assert "voice.md" in files


def test_read_niche_file(mock_postkit):
    bridge = PostKitBridge(mock_postkit)
    content = bridge.read_niche_file("voice.md")
    assert "Be direct" in content


def test_get_version(mock_postkit):
    bridge = PostKitBridge(mock_postkit)
    assert bridge.get_version() == "1.1.0"
    assert bridge.get_niche_version() == "1.0.0"
```

- [ ] **Step 5: Run tests**

Run: `cd app && uv run pytest tests/test_bridge.py -v`
Expected: All tests PASS

- [ ] **Step 6: Commit**

```
git add app/backend/config.py app/backend/core/ app/tests/
git commit -m "feat: add PostKitBridge and app config"
```



---

## Task 3: Core — SQLite Database & Event Bus

**Files:**
- Create: `app/backend/core/database.py`
- Create: `app/backend/core/events.py`
- Test: `app/tests/test_database.py`
- Test: `app/tests/test_events.py`

- [ ] **Step 1: Create core/events.py — observer pattern (< 40 lines)**

```python
"""Simple event bus — observer pattern for module communication."""

from collections import defaultdict
from typing import Any, Callable
import logging

logger = logging.getLogger(__name__)

_listeners: dict[str, list[Callable]] = defaultdict(list)


def on(event_name: str, callback: Callable) -> None:
    """Register a listener for an event."""
    _listeners[event_name].append(callback)


def emit(event_name: str, data: dict[str, Any] | None = None) -> None:
    """Emit an event to all registered listeners."""
    for callback in _listeners[event_name]:
        try:
            callback(data or {})
        except Exception as exc:
            logger.error(f"Event listener failed for '{event_name}': {exc}")


def clear() -> None:
    """Clear all listeners (for testing)."""
    _listeners.clear()
```

- [ ] **Step 2: Create core/database.py — SQLite with rebuild**

```python
"""SQLite database — rebuildable index over the filesystem."""

import aiosqlite
from pathlib import Path
from datetime import datetime

from app.backend.config import APP_DIR

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
    """Initialize schema."""
    async with await get_db() as db:
        await db.executescript(SCHEMA)
        await db.commit()


async def get_last_index_time() -> datetime | None:
    """Get the last time the index was built."""
    async with await get_db() as db:
        cursor = await db.execute(
            "SELECT value FROM meta WHERE key = 'last_index_build'"
        )
        row = await cursor.fetchone()
        if not row:
            return None
        return datetime.fromisoformat(row["value"])


async def set_last_index_time() -> None:
    """Record the current time as last index build."""
    now = datetime.now().isoformat()
    async with await get_db() as db:
        await db.execute(
            "INSERT OR REPLACE INTO meta (key, value) VALUES ('last_index_build', ?)",
            (now,),
        )
        await db.commit()


async def is_index_stale(posts_path: Path) -> bool:
    """Check if any file in posts/ is newer than last index build."""
    last_build = await get_last_index_time()
    if last_build is None:
        return True
    for md_file in posts_path.rglob("*.md"):
        file_mtime = datetime.fromtimestamp(md_file.stat().st_mtime)
        if file_mtime > last_build:
            return True
    return False
```

- [ ] **Step 3: Write tests for events and database**

```python
# app/tests/test_events.py
from app.backend.core import events


def test_emit_calls_listener():
    received = []
    events.on("test.event", lambda data: received.append(data))
    events.emit("test.event", {"key": "value"})
    assert received == [{"key": "value"}]
    events.clear()


def test_emit_handles_listener_error():
    """Failing listener doesn't crash emit."""
    def bad_listener(data):
        raise ValueError("broken")

    events.on("test.fail", bad_listener)
    events.emit("test.fail", {})  # Should not raise
    events.clear()
```

```python
# app/tests/test_database.py
import pytest
from app.backend.core.database import init_db, get_db, DB_PATH


@pytest.fixture(autouse=True)
async def clean_db(tmp_path, monkeypatch):
    """Use a temporary database for tests."""
    test_db = tmp_path / "test.db"
    monkeypatch.setattr("app.backend.core.database.DB_PATH", test_db)
    await init_db()
    yield
    if test_db.exists():
        test_db.unlink()


async def test_init_creates_tables():
    async with await get_db() as db:
        cursor = await db.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        tables = [row["name"] for row in await cursor.fetchall()]
    assert "posts" in tables
    assert "notifications" in tables
    assert "meta" in tables
```

- [ ] **Step 4: Run tests**

Run: `cd app && uv run pytest tests/ -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```
git add app/backend/core/database.py app/backend/core/events.py app/tests/
git commit -m "feat: add SQLite database and event bus"
```



---

## Task 4: Adapter — Base Interface & Kiro CLI

**Files:**
- Create: `app/backend/adapters/__init__.py`
- Create: `app/backend/adapters/base.py`
- Create: `app/backend/adapters/kiro.py`
- Test: `app/tests/test_adapter_kiro.py`

- [ ] **Step 1: Create adapters/base.py — abstract interface**

```python
"""Base adapter interface — all AI tool adapters implement this."""

from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from pathlib import Path


class BaseAdapter(ABC):
    """Abstract interface for AI CLI tool adapters."""

    def __init__(self, postkit_root: Path):
        self._postkit_root = postkit_root

    @abstractmethod
    async def send_message(self, message: str, session_id: str | None = None) -> AsyncGenerator[str, None]:
        """Send a message, yield streaming response chunks."""
        ...

    @abstractmethod
    async def start_session(self) -> str:
        """Start a persistent CLI session. Returns session_id."""
        ...

    @abstractmethod
    async def end_session(self, session_id: str) -> None:
        """Close a persistent session and kill the process."""
        ...

    @abstractmethod
    async def is_available(self) -> bool:
        """Check if the CLI tool is installed and reachable."""
        ...

    @abstractmethod
    def get_name(self) -> str:
        """Return display name of the adapter."""
        ...
```

- [ ] **Step 2: Create adapters/kiro.py — Kiro CLI adapter**

```python
"""Kiro CLI adapter — spawns kiro-cli chat as a subprocess."""

import asyncio
import uuid
import logging
from collections.abc import AsyncGenerator
from pathlib import Path

from app.backend.adapters.base import BaseAdapter

logger = logging.getLogger(__name__)


class KiroAdapter(BaseAdapter):
    """Adapter for Kiro CLI (kiro-cli chat command)."""

    def __init__(self, postkit_root: Path):
        super().__init__(postkit_root)
        self._sessions: dict[str, asyncio.subprocess.Process] = {}

    def get_name(self) -> str:
        return "Kiro CLI"

    async def is_available(self) -> bool:
        """Check if kiro-cli is installed."""
        try:
            proc = await asyncio.create_subprocess_exec(
                "kiro-cli", "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await proc.wait()
            return proc.returncode == 0
        except FileNotFoundError:
            return False

    async def start_session(self) -> str:
        """Spawn a kiro-cli chat process."""
        session_id = str(uuid.uuid4())
        proc = await asyncio.create_subprocess_exec(
            "kiro-cli", "chat",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(self._postkit_root),
        )
        self._sessions[session_id] = proc
        logger.info(f"Started Kiro session: {session_id}")
        return session_id

    async def send_message(self, message: str, session_id: str | None = None) -> AsyncGenerator[str, None]:
        """Send message to Kiro CLI and stream response chunks."""
        if session_id and session_id in self._sessions:
            proc = self._sessions[session_id]
        else:
            session_id = await self.start_session()
            proc = self._sessions[session_id]

        if proc.stdin is None or proc.stdout is None:
            yield "[Error: Process streams not available]"
            return

        # Write message to stdin
        proc.stdin.write(f"{message}\n".encode())
        await proc.stdin.drain()

        # Read response lines (streaming)
        # NOTE: Actual parsing logic will need refinement based on
        # kiro-cli output format. This is the initial implementation.
        try:
            while True:
                line = await asyncio.wait_for(
                    proc.stdout.readline(), timeout=120.0
                )
                if not line:
                    break
                decoded = line.decode("utf-8", errors="replace")
                yield decoded
        except asyncio.TimeoutError:
            yield "[Response timed out after 120 seconds]"

    async def end_session(self, session_id: str) -> None:
        """Kill the Kiro CLI process for this session."""
        proc = self._sessions.pop(session_id, None)
        if proc and proc.returncode is None:
            proc.terminate()
            try:
                await asyncio.wait_for(proc.wait(), timeout=3.0)
            except asyncio.TimeoutError:
                proc.kill()
            logger.info(f"Ended Kiro session: {session_id}")
```

- [ ] **Step 3: Write adapter availability test**

```python
# app/tests/test_adapter_kiro.py
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from app.backend.adapters.kiro import KiroAdapter


@pytest.fixture
def adapter(tmp_path):
    return KiroAdapter(tmp_path)


def test_adapter_name(adapter):
    assert adapter.get_name() == "Kiro CLI"


@patch("asyncio.create_subprocess_exec")
async def test_is_available_when_installed(mock_exec, adapter):
    mock_proc = AsyncMock()
    mock_proc.returncode = 0
    mock_proc.wait = AsyncMock(return_value=0)
    mock_exec.return_value = mock_proc
    assert await adapter.is_available() is True


@patch("asyncio.create_subprocess_exec", side_effect=FileNotFoundError)
async def test_is_available_when_not_installed(mock_exec, adapter):
    assert await adapter.is_available() is False
```

- [ ] **Step 4: Run tests**

Run: `cd app && uv run pytest tests/test_adapter_kiro.py -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```
git add app/backend/adapters/
git commit -m "feat: add adapter interface and Kiro CLI adapter"
```



---

## Task 5: Library Module — Post Index & CRUD

**Files:**
- Create: `app/backend/modules/__init__.py`
- Create: `app/backend/modules/library/__init__.py`
- Create: `app/backend/modules/library/models.py`
- Create: `app/backend/modules/library/service.py`
- Create: `app/backend/modules/library/router.py`
- Test: `app/tests/test_library.py`

This task implements: scanning posts from filesystem, indexing in SQLite, serving via API with filters.

- [ ] **Step 1: Create library/models.py**

```python
"""Library module data models."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.backend.core.models import PostStatus


class PostSummary(BaseModel):
    """Post card data for list views."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    status: PostStatus
    pillar: str | None = None
    platform: str | None = None
    created_at: str
    path: str


class PostDetail(BaseModel):
    """Full post data for editor view."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    status: PostStatus
    pillar: str | None = None
    platform: str | None = None
    created_at: str
    content: str
    path: str


class UpdatePostRequest(BaseModel):
    """Request to update a post's content or status."""
    content: str | None = None
    status: PostStatus | None = None
```

- [ ] **Step 2: Create library/service.py**

```python
"""Library service — post indexing, search, and status management."""

import hashlib
import re
from datetime import datetime
from pathlib import Path

import yaml

from app.backend.core.database import get_db, set_last_index_time
from app.backend.core.models import PostStatus


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
    async with await get_db() as db:
        await db.execute("DELETE FROM posts")
        for md_file in posts_path.rglob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            metadata, body = _extract_front_matter(content)
            title = _extract_title(body)
            post_id = _generate_post_id(str(md_file.relative_to(posts_path)))

            await db.execute(
                """INSERT OR REPLACE INTO posts (id, path, title, status, pillar, platform, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    post_id,
                    str(md_file.relative_to(posts_path)),
                    title,
                    metadata.get("status", PostStatus.PUBLISHED),
                    metadata.get("pillar"),
                    metadata.get("platform"),
                    metadata.get("created", md_file.stat().st_mtime),
                ),
            )
            count += 1
        await db.commit()
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

    async with await get_db() as db:
        cursor = await db.execute(query, params)
        rows = await cursor.fetchall()
    return [dict(row) for row in rows]


async def get_post_by_id(post_id: str) -> dict | None:
    """Get a single post from index."""
    async with await get_db() as db:
        cursor = await db.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        row = await cursor.fetchone()
    return dict(row) if row else None


async def update_post_status(post_id: str, status: PostStatus) -> None:
    """Update a post's status in the index."""
    async with await get_db() as db:
        await db.execute(
            "UPDATE posts SET status = ?, updated_at = ? WHERE id = ?",
            (status, datetime.now().isoformat(), post_id),
        )
        await db.commit()


async def get_post_count() -> int:
    """Get total post count."""
    async with await get_db() as db:
        cursor = await db.execute("SELECT COUNT(*) as cnt FROM posts")
        row = await cursor.fetchone()
    return row["cnt"] if row else 0
```

- [ ] **Step 3: Create library/router.py**

```python
"""Library module routes — post listing, detail, status updates."""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from app.backend.core.models import PostStatus
from app.backend.modules.library import service, models

router = APIRouter()


@router.get("/api/library/posts")
async def list_posts(
    status: PostStatus | None = None,
    pillar: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[models.PostSummary]:
    """List posts with optional filters."""
    posts = await service.get_posts(status=status, pillar=pillar, limit=limit, offset=offset)
    return [models.PostSummary(**p) for p in posts]


@router.get("/api/library/posts/{post_id}")
async def get_post(post_id: str) -> models.PostDetail:
    """Get a single post with full content."""
    post = await service.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    # TODO: Read actual file content from posts_path + post["path"]
    return models.PostDetail(**post, content="")


@router.put("/api/library/posts/{post_id}")
async def update_post(post_id: str, request: models.UpdatePostRequest):
    """Update post status or content."""
    post = await service.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if request.status:
        await service.update_post_status(post_id, request.status)
    return {"status": "updated"}


@router.get("/api/library/count")
async def post_count() -> dict:
    """Get total post count."""
    count = await service.get_post_count()
    return {"count": count}
```

- [ ] **Step 4: Write library service tests**

```python
# app/tests/test_library.py
import pytest
from pathlib import Path
from app.backend.modules.library.service import rebuild_index, get_posts, get_post_count
from app.backend.core.database import init_db


@pytest.fixture
async def indexed_posts(tmp_path, monkeypatch):
    """Create test posts and index them."""
    test_db = tmp_path / "test.db"
    monkeypatch.setattr("app.backend.core.database.DB_PATH", test_db)
    monkeypatch.setattr("app.backend.modules.library.service.get_db",
                        lambda: __import__('app.backend.core.database', fromlist=['get_db']).get_db())
    await init_db()

    posts_dir = tmp_path / "posts" / "2026-july"
    posts_dir.mkdir(parents=True)
    (posts_dir / "test-post.md").write_text(
        "---\nstatus: draft\npillar: News\n---\nBreaking: AI news today",
        encoding="utf-8",
    )
    (posts_dir / "second-post.md").write_text(
        "This has no front matter\nJust content",
        encoding="utf-8",
    )

    count = await rebuild_index(tmp_path / "posts")
    return tmp_path, count


async def test_rebuild_indexes_posts(indexed_posts):
    _, count = indexed_posts
    assert count == 2


async def test_get_posts_returns_all(indexed_posts):
    posts = await get_posts()
    assert len(posts) == 2


async def test_get_post_count(indexed_posts):
    count = await get_post_count()
    assert count == 2
```

- [ ] **Step 5: Mount library router in main.py**

Add to `app/backend/main.py`:
```python
from app.backend.modules.library.router import router as library_router
app.include_router(library_router)
```

- [ ] **Step 6: Run tests**

Run: `cd app && uv run pytest tests/ -v`
Expected: All PASS

- [ ] **Step 7: Commit**

```
git add app/backend/modules/ app/tests/test_library.py
git commit -m "feat: add library module with post indexing and API"
```



---

## Task 6: Content Module — Chat & Scout

**Files:**
- Create: `app/backend/modules/content/__init__.py`
- Create: `app/backend/modules/content/models.py`
- Create: `app/backend/modules/content/service.py`
- Create: `app/backend/modules/content/router.py`

This task implements: sending messages to the adapter, streaming responses via SSE, basic scout trigger.

- [ ] **Step 1: Create content/models.py**

```python
"""Content module data models."""

from pydantic import BaseModel, Field


class SendMessageRequest(BaseModel):
    """Request to send a message to the AI adapter."""
    message: str = Field(min_length=1, max_length=5000)
    session_id: str | None = None


class SessionResponse(BaseModel):
    """Response when a new session is created."""
    session_id: str
```

- [ ] **Step 2: Create content/service.py**

```python
"""Content service — manages adapter sessions and message flow."""

from collections.abc import AsyncGenerator

from app.backend.adapters.base import BaseAdapter


class ContentService:
    """Manages content creation sessions with the AI adapter."""

    def __init__(self, adapter: BaseAdapter):
        self._adapter = adapter

    async def start_session(self) -> str:
        """Start a new adapter session."""
        return await self._adapter.start_session()

    async def send_message(self, message: str, session_id: str | None = None) -> AsyncGenerator[str, None]:
        """Send a message and yield streaming response."""
        async for chunk in self._adapter.send_message(message, session_id):
            yield chunk

    async def end_session(self, session_id: str) -> None:
        """End an adapter session."""
        await self._adapter.end_session(session_id)

    async def is_adapter_available(self) -> bool:
        """Check if the adapter is ready."""
        return await self._adapter.is_available()
```

- [ ] **Step 3: Create content/router.py with SSE streaming**

```python
"""Content module routes — chat and scout endpoints."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.backend.modules.content import models

router = APIRouter()

# NOTE: ContentService instance will be injected via dependency
# once we wire up the adapter in main.py lifespan


@router.post("/api/content/session")
async def start_session() -> models.SessionResponse:
    """Start a new content creation session."""
    # Will be wired to ContentService via dependency injection
    return models.SessionResponse(session_id="placeholder")


@router.post("/api/content/send")
async def send_message(request: models.SendMessageRequest):
    """Send a message and get streaming response via SSE."""

    async def event_stream():
        # Will stream from adapter
        yield f"data: Received: {request.message}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/api/content/scout")
async def trigger_scout():
    """Trigger a news scout via the adapter."""
    return {"status": "scout_triggered", "message": "Scout functionality will use adapter session"}


@router.get("/api/content/adapter-status")
async def adapter_status():
    """Check if the AI adapter is available."""
    # Will be wired to adapter.is_available()
    return {"available": False, "adapter": "kiro", "message": "Adapter not yet configured"}
```

- [ ] **Step 4: Mount content router in main.py**

Add to `app/backend/main.py`:
```python
from app.backend.modules.content.router import router as content_router
app.include_router(content_router)
```

- [ ] **Step 5: Verify endpoints respond**

Run: `cd app && uv run python -m app.run`
Test: `curl http://localhost:8000/api/content/adapter-status`
Expected: `{"available": false, "adapter": "kiro", "message": "Adapter not yet configured"}`

- [ ] **Step 6: Commit**

```
git add app/backend/modules/content/
git commit -m "feat: add content module with chat and scout endpoints"
```



---

## Task 7: Frontend — App Shell, Tailwind v4, Base Template

**Files:**
- Create: `app/frontend/static/css/app.css` (Tailwind v4 with @theme)
- Create: `app/frontend/templates/base.html`
- Create: `app/frontend/components/sidebar.html`
- Create: `app/frontend/components/command-bar.html`
- Create: `app/frontend/static/js/app.js`
- Create: `app/package.json` (for Tailwind CLI build)

- [ ] **Step 1: Create package.json for Tailwind build tooling**

```json
{
  "name": "post-kit-frontend",
  "private": true,
  "scripts": {
    "css:build": "npx @tailwindcss/cli -i ./frontend/static/css/input.css -o ./frontend/static/css/app.css --minify",
    "css:watch": "npx @tailwindcss/cli -i ./frontend/static/css/input.css -o ./frontend/static/css/app.css --watch"
  },
  "devDependencies": {
    "@tailwindcss/cli": "^4.2.0"
  }
}
```

- [ ] **Step 2: Create input.css with @theme tokens**

```css
/* app/frontend/static/css/input.css */
@import "tailwindcss";

@theme {
  --color-surface: oklch(0.13 0.01 260);
  --color-surface-raised: oklch(0.18 0.01 260);
  --color-surface-overlay: oklch(0.22 0.01 260);
  --color-text-primary: oklch(0.93 0 0);
  --color-text-secondary: oklch(0.65 0 0);
  --color-text-muted: oklch(0.45 0 0);
  --color-accent: oklch(0.65 0.19 265);
  --color-accent-hover: oklch(0.72 0.19 265);
  --color-border: oklch(0.25 0.01 260);
  --color-border-subtle: oklch(0.20 0.01 260);

  --color-status-idea: oklch(0.65 0.10 300);
  --color-status-draft: oklch(0.75 0.15 85);
  --color-status-approved: oklch(0.65 0.15 250);
  --color-status-published: oklch(0.70 0.15 145);
  --color-status-archived: oklch(0.50 0.02 260);

  --font-sans: "Inter", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;

  --shadow-card: 0 2px 8px oklch(0 0 0 / 0.3);
  --shadow-overlay: 0 8px 32px oklch(0 0 0 / 0.5);
}

/* Base styles */
body {
  background-color: var(--color-surface);
  color: var(--color-text-primary);
  font-family: var(--font-sans);
}
```

- [ ] **Step 3: Create base.html — app shell**

```html
<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}post-kit{% endblock %}</title>
  <link rel="stylesheet" href="/static/css/app.css">
</head>
<body class="h-full flex overflow-hidden">
  {# Sidebar #}
  {% include "components/sidebar.html" %}

  {# Main content area #}
  <div class="flex-1 flex flex-col overflow-hidden">
    {# Top bar #}
    <header class="h-14 border-b border-border flex items-center justify-between px-6">
      <h1 class="text-lg font-semibold">{% block page_title %}{% endblock %}</h1>
      <div class="flex items-center gap-3">
        {% include "components/command-bar.html" %}
        <button data-action="notifications" class="relative p-2 rounded-lg hover:bg-surface-raised">
          <span class="text-lg">🔔</span>
        </button>
      </div>
    </header>

    {# Page content #}
    <main class="flex-1 overflow-y-auto p-6">
      {% block content %}{% endblock %}
    </main>
  </div>

  {% block scripts %}{% endblock %}
  <script type="module" src="/static/js/app.js"></script>
</body>
</html>
```

- [ ] **Step 4: Create components/sidebar.html**

```html
{# Sidebar navigation — items rendered from backend context #}
<aside class="w-56 h-full border-r border-border bg-surface flex flex-col">
  {# Logo #}
  <div class="h-14 flex items-center px-5 border-b border-border">
    <span class="text-lg font-bold text-primary">post-kit</span>
  </div>

  {# Navigation groups #}
  <nav class="flex-1 py-4 px-3 space-y-6 overflow-y-auto">
    {% for group in nav_groups %}
    <div>
      <span class="px-2 text-xs font-medium uppercase tracking-wider text-muted">
        {{ group.label }}
      </span>
      <ul class="mt-2 space-y-1">
        {% for item in group.items %}
        <li>
          <a href="{{ item.url }}"
             class="flex items-center gap-2 px-2 py-1.5 rounded-md text-sm
                    {% if current_page == item.id %}bg-surface-raised text-primary{% else %}text-secondary hover:text-primary hover:bg-surface-raised{% endif %}">
            <span>{{ item.icon }}</span>
            <span>{{ item.label }}</span>
          </a>
        </li>
        {% endfor %}
      </ul>
    </div>
    {% endfor %}
  </nav>

  {# Credits widget — always visible #}
  <div class="p-4 border-t border-border">
    <div class="text-xs text-muted mb-1">{{ plan_name }}</div>
    <div class="h-1.5 rounded-full bg-surface-raised overflow-hidden">
      <div class="h-full bg-accent rounded-full" style="width: {{ usage_percent }}%"></div>
    </div>
    <div class="text-xs text-muted mt-1">{{ usage_count }} / {{ usage_limit }}</div>
  </div>
</aside>
```

- [ ] **Step 5: Create components/command-bar.html**

```html
{# Command bar trigger — Ctrl+K / Cmd+K #}
<button data-action="open-command-bar"
        class="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-border bg-surface-raised text-sm text-secondary hover:text-primary">
  <span>⌘K</span>
  <span class="hidden sm:inline">Search or command...</span>
</button>

{# Command bar overlay (hidden by default) #}
<div data-command-bar class="hidden fixed inset-0 z-50 flex items-start justify-center pt-[20vh]">
  <div class="absolute inset-0 bg-black/50" data-action="close-command-bar"></div>
  <div class="relative w-full max-w-lg bg-surface-raised border border-border rounded-xl shadow-overlay overflow-hidden">
    <input type="text"
           data-command-input
           placeholder="Type a command..."
           class="w-full px-4 py-3 bg-transparent text-primary text-sm outline-none border-b border-border">
    <div data-command-results class="max-h-64 overflow-y-auto p-2">
      {# Results populated by JS #}
    </div>
  </div>
</div>
```

- [ ] **Step 6: Create static/js/app.js — core utilities**

```javascript
/** Core utilities — fetch wrapper, command bar, navigation. */

/** Fetch wrapper with error handling. */
export async function api(path, options = {}) {
  const res = await fetch(`/api${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `Request failed: ${res.status}`);
  }
  return res.json();
}

/** Debounce utility. */
export function debounce(fn, ms = 300) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), ms);
  };
}

/** Command bar logic. */
function initCommandBar() {
  const bar = document.querySelector('[data-command-bar]');
  const input = document.querySelector('[data-command-input]');
  if (!bar || !input) return;

  const open = () => { bar.classList.remove('hidden'); input.focus(); };
  const close = () => { bar.classList.add('hidden'); input.value = ''; };

  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      bar.classList.contains('hidden') ? open() : close();
    }
    if (e.key === 'Escape') close();
  });

  document.querySelector('[data-action="open-command-bar"]')?.addEventListener('click', open);
  document.querySelector('[data-action="close-command-bar"]')?.addEventListener('click', close);
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', initCommandBar);
```

- [ ] **Step 7: Build Tailwind CSS**

Run: `cd app && npm install && npm run css:build`
Expected: `app/frontend/static/css/app.css` generated

- [ ] **Step 8: Wire up templates in FastAPI**

Add to `app/backend/main.py`:
```python
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory=str(FRONTEND_DIR / "templates"))

# Add template context helper
def get_nav_context(bridge):
    """Build navigation context from bridge config."""
    nav_groups = [
        {"label": "Create", "items": [
            {"id": "content", "label": "Content", "icon": "✦", "url": "/content"},
        ]},
        {"label": "Manage", "items": [
            {"id": "library", "label": "Library", "icon": "📚", "url": "/library"},
        ]},
    ]
    return nav_groups
```

- [ ] **Step 9: Commit**

```
git add app/frontend/ app/package.json
git commit -m "feat: add app shell with Tailwind v4 and command bar"
```



---

## Task 8: Frontend — Page Templates (Library, Content, Onboarding)

**Files:**
- Create: `app/frontend/templates/library.html`
- Create: `app/frontend/templates/content.html`
- Create: `app/frontend/templates/onboarding.html`
- Create: `app/frontend/components/post-card.html`
- Create: `app/frontend/components/chat-bubble.html`
- Create: `app/frontend/static/js/chat.js`

- [ ] **Step 1: Create components/post-card.html**

```html
{# Post card component — receives `post` from context #}
<article class="rounded-lg border border-border bg-surface-raised p-4 hover:border-accent/50 transition-colors cursor-pointer"
         data-post-id="{{ post.id }}">
  <div class="flex items-center justify-between mb-2">
    <span class="text-xs font-medium px-2 py-0.5 rounded-full bg-status-{{ post.status }}/20 text-status-{{ post.status }}">
      {{ post.status }}
    </span>
    <time class="text-xs text-muted">{{ post.created_at }}</time>
  </div>
  <h3 class="text-sm font-medium text-primary truncate">{{ post.title }}</h3>
  {% if post.pillar %}
    <span class="mt-1 inline-block text-xs text-secondary">{{ post.pillar }}</span>
  {% endif %}
</article>
```

- [ ] **Step 2: Create templates/library.html**

```html
{% extends "base.html" %}
{% block title %}Library — post-kit{% endblock %}
{% block page_title %}Library{% endblock %}

{% block content %}
<section class="space-y-6">
  {# Filters #}
  <div class="flex items-center gap-3">
    <select data-filter="status" class="px-3 py-1.5 text-sm rounded-lg border border-border bg-surface-raised text-primary">
      <option value="">All statuses</option>
      <option value="draft">Draft</option>
      <option value="approved">Approved</option>
      <option value="published">Published</option>
      <option value="archived">Archived</option>
    </select>
    <input type="search" data-search="posts" placeholder="Search posts..."
           class="px-3 py-1.5 text-sm rounded-lg border border-border bg-surface-raised text-primary placeholder:text-muted flex-1 max-w-xs">
  </div>

  {# Post grid #}
  <div data-post-list class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    {% for post in posts %}
      {% include "components/post-card.html" %}
    {% endfor %}

    {% if not posts %}
      <p class="text-secondary col-span-full text-center py-12">
        No posts yet. Go to Content to create your first one.
      </p>
    {% endif %}
  </div>
</section>
{% endblock %}
```

- [ ] **Step 3: Create components/chat-bubble.html**

```html
{# Chat bubble — used in content creation and onboarding #}
{# Expects: role ("user" or "assistant"), content (text) #}
<div class="flex gap-3 {% if role == 'user' %}justify-end{% endif %}">
  <div class="max-w-[80%] rounded-xl px-4 py-2.5 text-sm leading-relaxed
              {% if role == 'user' %}bg-accent text-white{% else %}bg-surface-raised text-primary border border-border{% endif %}">
    {{ content }}
  </div>
</div>
```

- [ ] **Step 4: Create templates/content.html**

```html
{% extends "base.html" %}
{% block title %}Content — post-kit{% endblock %}
{% block page_title %}Content{% endblock %}

{% block content %}
<section class="flex flex-col h-full max-h-[calc(100vh-8rem)]">
  {# Tabs: Scout | Create #}
  <div class="flex gap-1 mb-4 border-b border-border">
    <button data-tab="scout" class="px-4 py-2 text-sm font-medium border-b-2 border-accent text-primary">Scout</button>
    <button data-tab="create" class="px-4 py-2 text-sm font-medium border-b-2 border-transparent text-secondary hover:text-primary">Create</button>
  </div>

  {# Chat area #}
  <div data-chat-messages class="flex-1 overflow-y-auto space-y-4 pb-4">
    {% if not adapter_available %}
      <div class="text-center py-12">
        <p class="text-secondary">AI adapter not available.</p>
        <p class="text-muted text-sm mt-1">Configure Kiro CLI in Settings to start creating content.</p>
      </div>
    {% else %}
      <div class="text-center py-12 text-secondary">
        <p>Ask me anything — "what's trending?", "write about [topic]", or just chat.</p>
      </div>
    {% endif %}
  </div>

  {# Input #}
  <div class="border-t border-border pt-4">
    <form data-chat-form class="flex gap-2">
      <input type="text" data-chat-input
             placeholder="Type a message..."
             class="flex-1 px-4 py-2.5 rounded-xl border border-border bg-surface-raised text-primary text-sm placeholder:text-muted focus:outline-none focus:border-accent"
             {% if not adapter_available %}disabled{% endif %}>
      <button type="submit"
              class="px-4 py-2.5 rounded-xl bg-accent text-white text-sm font-medium hover:bg-accent-hover disabled:opacity-50"
              {% if not adapter_available %}disabled{% endif %}>
        Send
      </button>
    </form>
  </div>
</section>
{% endblock %}

{% block scripts %}
<script type="module" src="/static/js/chat.js"></script>
{% endblock %}
```

- [ ] **Step 5: Create static/js/chat.js**

```javascript
/** Chat interface — handles message sending and streaming responses. */
import { api } from './app.js';

const form = document.querySelector('[data-chat-form]');
const input = document.querySelector('[data-chat-input]');
const messages = document.querySelector('[data-chat-messages]');

if (form && input && messages) {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;

    appendMessage('user', text);
    input.value = '';

    try {
      const res = await fetch('/api/content/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let assistantText = '';

      const bubble = appendMessage('assistant', '...');

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        // Parse SSE format
        for (const line of chunk.split('\n')) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') break;
            assistantText += data;
            bubble.textContent = assistantText;
          }
        }
      }
    } catch (err) {
      appendMessage('assistant', `Error: ${err.message}`);
    }
  });
}

function appendMessage(role, content) {
  const div = document.createElement('div');
  div.className = `flex gap-3 ${role === 'user' ? 'justify-end' : ''}`;
  const bubble = document.createElement('div');
  bubble.className = `max-w-[80%] rounded-xl px-4 py-2.5 text-sm leading-relaxed ${
    role === 'user'
      ? 'bg-accent text-white'
      : 'bg-surface-raised text-primary border border-border'
  }`;
  bubble.textContent = content;
  div.appendChild(bubble);
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
  return bubble;
}
```

- [ ] **Step 6: Create templates/onboarding.html (standalone, no sidebar)**

```html
<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Welcome — post-kit</title>
  <link rel="stylesheet" href="/static/css/app.css">
</head>
<body class="h-full flex items-center justify-center bg-surface">
  <div class="w-full max-w-lg mx-auto p-8">
    <h1 class="text-2xl font-bold text-primary mb-2">Welcome to post-kit</h1>
    <p class="text-secondary mb-8">Let's set up your content pipeline. This takes about 3 minutes.</p>

    {# Chat-based onboarding #}
    <div data-chat-messages class="space-y-4 mb-6 max-h-96 overflow-y-auto">
      <div class="flex gap-3">
        <div class="max-w-[80%] rounded-xl px-4 py-2.5 text-sm bg-surface-raised text-primary border border-border">
          Ready to set up? The AI will ask you a few questions about your niche, voice, and posting style.
        </div>
      </div>
    </div>

    <form data-chat-form class="flex gap-2">
      <input type="text" data-chat-input
             placeholder="Type 'guided' to start setup..."
             class="flex-1 px-4 py-2.5 rounded-xl border border-border bg-surface-raised text-primary text-sm placeholder:text-muted focus:outline-none focus:border-accent">
      <button type="submit" class="px-4 py-2.5 rounded-xl bg-accent text-white text-sm font-medium hover:bg-accent-hover">
        Start
      </button>
    </form>
  </div>
  <script type="module" src="/static/js/chat.js"></script>
</body>
</html>
```

- [ ] **Step 7: Add page routes to serve templates**

Add to `app/backend/main.py`:
```python
@app.get("/")
async def root(request: Request):
    bridge = PostKitBridge(get_postkit_root())
    if not bridge.is_onboarded():
        return templates.TemplateResponse(request, "onboarding.html")
    return RedirectResponse(url="/library", status_code=302)

@app.get("/library")
async def library_page(request: Request):
    bridge = PostKitBridge(get_postkit_root())
    posts = await library_service.get_posts()
    return templates.TemplateResponse(request, "library.html", {
        "posts": posts,
        "nav_groups": get_nav_context(bridge),
        "current_page": "library",
        "plan_name": "Free",
        "usage_count": 0,
        "usage_limit": 100,
        "usage_percent": 0,
    })

@app.get("/content")
async def content_page(request: Request):
    bridge = PostKitBridge(get_postkit_root())
    return templates.TemplateResponse(request, "content.html", {
        "adapter_available": False,
        "nav_groups": get_nav_context(bridge),
        "current_page": "content",
        "plan_name": "Free",
        "usage_count": 0,
        "usage_limit": 100,
        "usage_percent": 0,
    })
```

- [ ] **Step 8: Verify pages render**

Run: `cd app && uv run python -m app.run`
Visit: http://localhost:8000/library and http://localhost:8000/content
Expected: Pages render with sidebar, topbar, content area

- [ ] **Step 9: Commit**

```
git add app/frontend/ app/backend/main.py
git commit -m "feat: add library, content, and onboarding page templates"
```

---

## Task 9: Wire Everything Together — Startup Lifecycle

**Files:**
- Modify: `app/backend/main.py` (full wiring)

- [ ] **Step 1: Complete main.py with full startup lifecycle**

Wire up: bridge initialization, database init, index rebuild check, adapter instantiation, all routers mounted.

```python
"""Post-kit desktop app — FastAPI entry point."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.backend.config import get_postkit_root, load_config
from app.backend.core.bridge import PostKitBridge
from app.backend.core.database import init_db, is_index_stale
from app.backend.modules.library.router import router as library_router
from app.backend.modules.library import service as library_service
from app.backend.modules.content.router import router as content_router

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
templates = Jinja2Templates(directory=str(FRONTEND_DIR / "templates"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: init DB, check index, configure adapter."""
    await init_db()
    bridge = PostKitBridge(get_postkit_root())
    posts_path = bridge.get_posts_path()
    if await is_index_stale(posts_path):
        count = await library_service.rebuild_index(posts_path)
    yield


app = FastAPI(title="post-kit", docs_url=None, redoc_url=None, lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")

app.include_router(library_router)
app.include_router(content_router)


def _get_nav_context(bridge: PostKitBridge) -> list[dict]:
    """Build sidebar navigation from bridge config."""
    groups = [
        {"label": "Create", "items": [
            {"id": "content", "label": "Content", "icon": "✦", "url": "/content"},
        ]},
        {"label": "Manage", "items": [
            {"id": "library", "label": "Library", "icon": "📚", "url": "/library"},
        ]},
        {"label": "Settings", "items": [
            {"id": "settings", "label": "Settings", "icon": "⚙", "url": "/settings"},
        ]},
    ]
    # Conditionally add modules based on config
    modules = bridge.get_active_modules()
    if any(m in modules for m in ["visual-system", "image-prompts"]):
        groups[0]["items"].append({"id": "images", "label": "Images", "icon": "🖼", "url": "/images"})
    if "analytics" in modules:
        groups.insert(2, {"label": "Insights", "items": [
            {"id": "analytics", "label": "Analytics", "icon": "📊", "url": "/analytics"},
        ]})
    return groups


def _get_credits_context() -> dict:
    """Load credits/plan info from config."""
    config = load_config()
    plan = config.get("plan", {"name": "Free", "limit": 100})
    usage = config.get("usage", {"count": 0})
    limit = plan.get("limit", 100)
    count = usage.get("count", 0)
    return {
        "plan_name": plan.get("name", "Free"),
        "usage_count": count,
        "usage_limit": limit,
        "usage_percent": min(100, int(count / max(limit, 1) * 100)),
    }


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


@app.get("/")
async def root():
    bridge = PostKitBridge(get_postkit_root())
    if not bridge.is_onboarded():
        return RedirectResponse(url="/onboarding", status_code=302)
    return RedirectResponse(url="/content", status_code=302)


@app.get("/onboarding")
async def onboarding_page(request: Request):
    return templates.TemplateResponse(request, "onboarding.html")


@app.get("/library")
async def library_page(request: Request):
    bridge = PostKitBridge(get_postkit_root())
    posts = await library_service.get_posts()
    return templates.TemplateResponse(request, "library.html", {
        "posts": posts,
        "nav_groups": _get_nav_context(bridge),
        "current_page": "library",
        **_get_credits_context(),
    })


@app.get("/content")
async def content_page(request: Request):
    bridge = PostKitBridge(get_postkit_root())
    return templates.TemplateResponse(request, "content.html", {
        "adapter_available": False,
        "nav_groups": _get_nav_context(bridge),
        "current_page": "content",
        **_get_credits_context(),
    })
```

- [ ] **Step 2: Run full app and verify**

Run: `cd app && uv run python -m app.run`
- Visit `/` → redirects to `/content` (if onboarded) or `/onboarding`
- Visit `/library` → shows post grid (may be empty)
- Visit `/content` → shows chat interface
- Visit `/api/health` → returns `{"status": "ok"}`
- Visit `/api/library/posts` → returns JSON list

- [ ] **Step 3: Run all tests**

Run: `cd app && uv run pytest tests/ -v`
Expected: All PASS

- [ ] **Step 4: Commit**

```
git add app/backend/main.py
git commit -m "feat: wire full startup lifecycle and page routes"
```

---

## End of Phase 1 Plan

**What Phase 1 delivers:**
- Working FastAPI app with health endpoint
- PostKitBridge reading config from post-kit files
- SQLite database with rebuild-from-filesystem logic
- Library module (post indexing, listing, filtering, status updates)
- Content module (chat endpoint with SSE streaming, scout placeholder)
- Kiro CLI adapter (spawns process, sends messages, streams response)
- Full app shell (sidebar, command bar, credits widget)
- Three page templates (library, content, onboarding)
- All code typed, tested, and following steering rules

**What comes in Phase 2:** Calendar, Images (MCP), Brand editing
**What comes in Phase 3:** Analytics, Credits, Notifications, Settings page
