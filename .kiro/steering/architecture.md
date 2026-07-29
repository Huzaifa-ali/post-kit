# Project Architecture Rules

## Core Principles

1. **Filesystem is truth.** SQLite is a rebuildable index. If the DB is deleted, the app rebuilds from files on next startup.
2. **Nothing hardcoded.** The app renders whatever the user's config defines. No niche-specific knowledge in code.
3. **PostKitBridge is the boundary.** Only `core/bridge.py` reads/writes post-kit files (`engine/`, `my-niche/`, `posts/`). All other code goes through bridge methods.
4. **Modules are independent.** No cross-module imports. Communication via event bus only.
5. **Adapter is opaque.** The app sends plain text, receives plain text. It doesn't know how the AI tool works internally.

## Module Structure

Every module follows this layout:

```
modules/<name>/
├── router.py    # FastAPI routes (HTTP layer only)
├── service.py   # Business logic (no FastAPI imports)
└── models.py    # Pydantic request/response models
```

- Router calls service. Service calls bridge/database/adapter as needed.
- No service calls another module's service directly.
- If module A needs to react to module B's action → event bus.

## Adding a New Module

1. Create `app/backend/modules/<name>/` with router.py, service.py, models.py
2. Mount router in `main.py`
3. Create `app/frontend/templates/<name>.html`
4. Add conditional nav item in `components/sidebar.html`
5. No existing code modified.

## Adding a New Adapter

1. Create `app/backend/adapters/<name>.py` implementing `BaseAdapter`
2. Register in `config.py` as a selectable option
3. No other code changes needed.

## File Naming

- Python: `snake_case.py`
- Templates: `snake_case.html`
- JS: `camelCase.js` or `kebab-case.js` (pick one, stay consistent — prefer `app.js`, `chat.js`)
- CSS: `app.css` (single compiled file)
- Components: `kebab-case.html` (e.g., `post-card.html`, `chat-bubble.html`)

## What Lives Where

| Concern | Location |
|---------|----------|
| Post-kit file reading/writing | `core/bridge.py` only |
| Database operations | `core/database.py` + module services |
| AI tool communication | `adapters/` |
| MCP integration | `mcp/` |
| HTTP endpoints | Module `router.py` files |
| Business logic | Module `service.py` files |
| Data shapes | Module `models.py` files |
| Shared models (enums, base) | `core/models.py` |
| App configuration | `config.py` + `app/data/config.json` |
| Frontend pages | `frontend/templates/` |
| Reusable HTML fragments | `frontend/components/` |
| Client-side behavior | `frontend/static/js/` |
| Styling | Tailwind classes in HTML (compiled to `static/css/app.css`) |

## Anti-Patterns (Never Do)

- ❌ Import from one module into another module
- ❌ Read post-kit files (`my-niche/`, `engine/`, `posts/`) outside of bridge.py
- ❌ Hardcode pillar names, platform names, module names, or any niche-specific strings
- ❌ Put business logic in router files
- ❌ Put FastAPI imports in service files
- ❌ Use raw SQL without parameterized queries
- ❌ Modify files in `engine/` from app code
- ❌ Assume specific fields exist in niche.yaml (always check, handle missing gracefully)
- ❌ Create God objects or utility files that grow unbounded
- ❌ Skip type hints
