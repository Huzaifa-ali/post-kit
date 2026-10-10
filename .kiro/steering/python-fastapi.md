---
inclusion: fileMatch
fileMatchPattern: "app/backend/**/*.py"
---

# Python & FastAPI — Code Standards

Write code like Netflix Dispatch, Starlette, and encode/httpx: clean, obvious, boring in the best way.

## Single Responsibility

Every function does ONE thing. Every file has ONE purpose. Every class has ONE reason to change.

- A function that fetches data does not also format it.
- A function that validates does not also save.
- A file with routes does not contain business logic.
- A file with business logic does not import FastAPI.

**The test:** Can you describe what this function/file does in one sentence without using "and"? If not, split it.

**Function length:** If a function exceeds 20-25 lines, it's probably doing two things. Extract the second thing.

**File length:** If a file exceeds 200 lines, it has too many responsibilities. Split by concern.

## How Top-Tier Repos Write Python

### Naming tells you everything
```python
# Bad — what does this do?
def process(data):
    ...

# Good — name IS the documentation
def parse_front_matter_from_markdown(content: str) -> dict[str, str]:
    ...
```

- Functions: verb + noun (`get_posts`, `parse_config`, `emit_event`, `rebuild_index`)
- Variables: descriptive nouns (`post_content`, `active_modules`, `niche_config`)
- Booleans: `is_` / `has_` / `can_` prefix (`is_onboarded`, `has_analytics`, `can_scout`)
- Constants: `UPPER_SNAKE` (`MAX_RETRY_COUNT`, `DEFAULT_PORT`)
- Private: `_underscore_prefix` (internal, don't call from outside)

### Small, focused modules
```
# How Netflix Dispatch structures a domain:
module/
├── router.py       # HTTP in/out only — thin
├── service.py      # All logic — thick
├── models.py       # Data shapes — Pydantic schemas
```

Router is thin (10-50 lines per endpoint). Service is where the work happens. Models define the contract.

### Type everything
```python
# Every function signature is fully typed
async def get_posts_by_status(
    status: PostStatus,
    limit: int = 50,
    offset: int = 0,
) -> list[PostSummary]:
    ...
```

No `Any`. No untyped parameters. No untyped returns. The types ARE the documentation.

### Dependency injection over global state
```python
# Bad — hidden dependency
from app.core.database import db  # module-level import of live connection

async def get_post(post_id: int):
    return await db.fetch(...)

# Good — explicit dependency, testable
async def get_post(
    post_id: int,
    db: Database = Depends(get_db),
) -> PostResponse:
    ...
```

### Errors are explicit
```python
# Each module defines its own exceptions
class PostNotFound(Exception):
    def __init__(self, post_id: str):
        self.post_id = post_id
        super().__init__(f"Post not found: {post_id}")

# Service raises domain exceptions
async def get_post(post_id: str) -> Post:
    post = await db.fetch_post(post_id)
    if not post:
        raise PostNotFound(post_id)
    return post

# Router converts to HTTP
@router.get("/posts/{post_id}")
async def get_post_endpoint(post_id: str):
    try:
        return await service.get_post(post_id)
    except PostNotFound:
        raise HTTPException(status_code=404, detail="Post not found")
```

### No magic, no cleverness
```python
# Bad — clever metaclass magic nobody understands
class AutoRouter(metaclass=RouterMeta):
    ...

# Good — obvious and boring
router = APIRouter(prefix="/api/library", tags=["library"])

@router.get("/posts")
async def list_posts(...):
    ...
```

## FastAPI Specific

### Async Rules
- `async def` for I/O (file, network, DB, subprocess)
- `def` for pure computation (sync routes auto-run in threadpool)
- Never `time.sleep()` in async. Use `asyncio.sleep()`.
- Never sync file I/O in async. Use `aiofiles` or `run_in_threadpool`.

### Pydantic v2 Patterns
```python
from pydantic import BaseModel, ConfigDict, Field
from enum import StrEnum

class PostStatus(StrEnum):
    IDEA = "idea"
    DRAFT = "draft"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    title: str
    status: PostStatus
    created_at: datetime
    pillar: str | None = None
    platform: str | None = None

class CreatePostRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=500)
    platform: str | None = None
```

- Separate request models from response models. Always.
- Use `Field()` for validation constraints.
- Use `StrEnum` for fixed-value fields.
- `model_config = ConfigDict(from_attributes=True)` when mapping from DB rows.

### Route conventions
```python
# API routes (return JSON)
@router.get("/api/library/posts")
@router.post("/api/content/scout")

# Page routes (return HTML)
@router.get("/library")
@router.get("/content")
```

### Database (aiosqlite)
```python
# Context manager — connection always closes
async def get_db():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        yield db

# Parameterized queries — ALWAYS
await db.execute(
    "SELECT * FROM posts WHERE status = ? AND created_at > ?",
    (status, since_date),
)

# Never this:
await db.execute(f"SELECT * FROM posts WHERE status = '{status}'")  # SQL INJECTION
```

## Code Review Checklist

Before any code is committed, it must pass:

- [ ] Every function does one thing (describable without "and")
- [ ] Every function is under 25 lines
- [ ] Every file is under 200 lines
- [ ] All function signatures have complete type hints
- [ ] No business logic in router files
- [ ] No FastAPI imports in service files
- [ ] No raw SQL concatenation (parameterized only)
- [ ] No global mutable state
- [ ] No `print()` statements (use `logging`)
- [ ] No commented-out code
- [ ] Error cases are handled explicitly
- [ ] Names are self-documenting (no abbreviations unless universal like `db`, `id`, `url`)
