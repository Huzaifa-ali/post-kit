---
inclusion: fileMatch
fileMatchPattern: "app/backend/**/*.py"
---

# Python & FastAPI Standards (2026)

## Python (3.12+)

- Use modern syntax: `match/case`, type union `X | Y | None`, `StrEnum`, `TypeAlias`.
- Type hints on ALL function signatures — parameters AND return types. No `Any` unless genuinely unavoidable.
- Use `pathlib.Path` for all file/path operations. Never `os.path`.
- f-strings for formatting. Never `.format()` or `%`.
- Imports ordered: stdlib → third-party → local. One blank line between groups.
- No wildcard imports (`from x import *`).
- Docstrings on all public functions/classes. One-liner for simple, Google-style multi-line for complex.
- Use `ruff` for linting and formatting. No black, isort, or flake8 separately.

## Async Rules

- `async def` for ANY function that does I/O (file, network, database, subprocess).
- `def` (sync) for pure computation with zero I/O.
- Never block the event loop: no `time.sleep()`, no sync file reads, no sync HTTP in async routes.
- If you must call a sync library from an async context, use `run_in_threadpool` from Starlette.
- Sync route functions are OK for simple endpoints — FastAPI runs them in threadpool automatically.
- But prefer `async def` with proper `await` calls when possible.

## FastAPI Patterns

### Module Structure
Each module: `router.py` (endpoints) + `service.py` (logic) + `models.py` (Pydantic schemas).

- **router.py** — HTTP layer only. Parse request, call service, format response. No business logic.
- **service.py** — All logic. No FastAPI imports. Pure Python. Testable independently.
- **models.py** — Pydantic v2 models for request/response. Use `model_config = ConfigDict(...)`.

### Dependency Injection
- Use `Depends()` for shared resources (DB session, bridge instance, adapter, current config).
- Chain dependencies: e.g., `valid_post_id` → `valid_owned_post`.
- Dependencies are cached per-request — safe to use the same dep in multiple places.
- Prefer async dependencies over sync (sync runs in threadpool = overhead).

### Pydantic v2
- Use `BaseModel` for all request/response schemas. Never pass raw dicts across boundaries.
- Field validation: use `Field(min_length=1, max_length=255)`, `field_validator`, `model_validator`.
- Use `StrEnum` for string enumerations (PostStatus, Platform, etc.).
- Custom base model for app-wide serialization defaults (datetime format, etc.).
- Separate request models from response models — never reuse the same model for both.

### Route Conventions
- API routes: `POST /api/{module}/{action}` — e.g., `/api/library/posts`, `/api/content/scout`
- Page routes: `GET /{page}` — e.g., `/library`, `/content`, `/settings`
- Use `response_model` on all API routes for auto-documentation.
- Set explicit `status_code` on creation endpoints (201).
- Use `tags` for grouping in auto-docs.

### Error Handling
- Service functions raise domain exceptions (e.g., `PostNotFound`, `AdapterUnavailable`).
- Routers catch and convert to `HTTPException` with appropriate status codes.
- Never swallow exceptions. Log with proper context, then raise or return error.
- Structured error response: `{"detail": "message", "code": "ERROR_CODE"}`

### Database (aiosqlite)
- Context managers for connections: `async with get_db() as db:`
- Parameterized queries always. Never f-string or concatenate SQL.
- WAL mode for concurrent reads.
- Migrations: ordered list of SQL statements, run on startup, skip if already applied (try/except on ALTER).
- Keep queries in service layer, not in router.

## Naming

- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private: `_single_underscore_prefix`
- Pydantic models: `PascalCase` with descriptor suffix (`PostResponse`, `CreatePostRequest`, `PostStatus`)
- Router instances: `router = APIRouter()`
- Service functions: verb-first (`get_posts`, `create_post`, `update_status`)

## Testing

- Use `pytest` + `httpx` with `ASGITransport` for async integration tests.
- Use `dependency_overrides` to mock dependencies in tests — not monkeypatch.
- Test the service layer independently from routers.
- One test file per module in a `tests/` directory mirroring the module structure.

## Dependencies (pinned in pyproject.toml)

```
fastapi
uvicorn[standard]
jinja2
python-multipart
openpyxl
aiosqlite
pyyaml
markdown
httpx          # for testing
pytest
pytest-asyncio
ruff           # linting + formatting
```
