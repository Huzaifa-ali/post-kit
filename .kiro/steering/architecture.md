# Project Architecture — Single Responsibility at Every Level

How top-tier open source projects stay maintainable: every piece has one job, clear boundaries, and obvious names.

## The Principle

**Single responsibility applies at every level:**
- System level: each layer has one job (Tauri=shell, FastAPI=logic, Frontend=display)
- Module level: each module owns one feature completely
- File level: each file has one purpose
- Function level: each function does one thing
- Line level: each line is readable without context

**If you can't explain it in one sentence, it's too complex. Split it.**

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│ Tauri Shell                                          │
│ Job: Launch backend, show webview, handle OS events  │
└─────────────────────┬───────────────────────────────┘
                      │ spawns
┌─────────────────────▼───────────────────────────────┐
│ FastAPI Backend                                      │
│ Job: All application logic, serve HTML, expose API   │
├──────────────────────────────────────────────────────┤
│ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│ │ Modules  │ │   Core   │ │ Adapters │             │
│ │ (features│ │ (shared) │ │ (AI CLI) │             │
│ └──────────┘ └──────────┘ └──────────┘             │
└─────────────────────┬───────────────────────────────┘
                      │ reads/writes
┌─────────────────────▼───────────────────────────────┐
│ Filesystem (post-kit)                                │
│ Job: Source of truth — posts, config, engine         │
└─────────────────────────────────────────────────────┘
```

## Module Rules

Every module follows this structure:

```
modules/<name>/
├── router.py    # HTTP in/out. Thin. Calls service.
├── service.py   # Logic. Thick. The brain.
└── models.py    # Pydantic schemas. The contract.
```

| File | Allowed to import | NOT allowed to import |
|------|-------------------|----------------------|
| router.py | FastAPI, own service, own models | Other modules, database directly |
| service.py | core/bridge, core/database, core/events | FastAPI, other modules |
| models.py | Pydantic, stdlib | Anything else |

**Module isolation test:** Delete any module folder. The app still starts (minus that feature). If it doesn't, you have coupling.

## Core (Shared Layer)

```
core/
├── bridge.py     # Reads/writes post-kit files. THE boundary.
├── database.py   # SQLite connection, migrations, rebuild.
├── events.py     # Simple observer pattern (< 50 lines).
└── models.py     # Shared enums and base models only.
```

- Bridge is the ONLY code touching `my-niche/`, `engine/`, `posts/`.
- Database is the ONLY code touching `postkit.db`.
- Events is glue — modules emit, other modules listen. No direct calls across.

## Boundaries (What Can Call What)

```
Router → Service → Bridge/Database/Adapter/Events
                ↗
Frontend → Router (via HTTP)

Module A ─── ✗ ───→ Module B (NEVER direct)
Module A ──event──→ Events ──event──→ Module B (OK)
```

## Naming That Works

### Files
- Python: `snake_case.py` — name = purpose (`bridge.py`, `post_service.py`)
- Templates: `snake_case.html` — name = page (`library.html`, `content.html`)
- Components: `kebab-case.html` — name = thing (`post-card.html`, `chat-bubble.html`)
- JS: `kebab-case.js` or simple names (`app.js`, `chat.js`, `editor.js`)

### Code
- Classes: `PascalCase` — nouns (`PostKitBridge`, `KiroAdapter`, `PostResponse`)
- Functions: `snake_case` — verb + noun (`get_posts`, `rebuild_index`, `emit_event`)
- Variables: `snake_case` — descriptive nouns (`active_modules`, `niche_config`)
- Constants: `UPPER_SNAKE` — (`DB_PATH`, `DEFAULT_PORT`, `MAX_RETRIES`)
- Booleans: `is_/has_/can_` prefix (`is_onboarded`, `has_analytics`)

## How to Add Things

### New feature/module
1. Create `app/backend/modules/<name>/` with router.py + service.py + models.py
2. Mount router in `main.py` (one line)
3. Create `app/frontend/templates/<name>.html`
4. Add nav item conditionally in sidebar component
5. Zero changes to existing code

### New adapter
1. Create `app/backend/adapters/<name>.py` implementing `BaseAdapter`
2. Add to config options
3. Zero changes to existing code

### New component
1. Create `app/frontend/components/<name>.html`
2. `{% include %}` where needed
3. Zero changes to existing components

## Anti-Patterns (What Top-Tier Repos Never Do)

- ❌ God files (over 200 lines)
- ❌ God functions (over 25 lines)
- ❌ Cross-module imports
- ❌ Business logic in routers or templates
- ❌ Hardcoded values that belong in config
- ❌ Global mutable state
- ❌ Implicit dependencies (import at module level, use silently)
- ❌ Abbreviations in names (except universal: `db`, `id`, `url`, `config`)
- ❌ Commented-out code
- ❌ Dead code (unreachable, unused imports, unused functions)
- ❌ Nested callbacks or deeply nested conditionals (> 2 levels)
- ❌ Mixing concerns in one function (fetch AND render, validate AND save)
- ❌ Magic strings/numbers (use constants or enums)

## The Quality Bar

This is open source. Contributors will read this code. Every file should be:

1. **Obvious** — a new contributor understands it in 30 seconds
2. **Focused** — does one thing, named to reflect that thing
3. **Independent** — deletable without breaking unrelated code
4. **Tested** — if it has logic, it has a test
5. **Documented** — docstring on public functions, comments only for "why" (never "what")
