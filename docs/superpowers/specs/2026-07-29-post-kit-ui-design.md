# Post-Kit Desktop UI — Design Spec

**Date:** 2026-07-29  
**Status:** Approved  
**Branch:** feat/web-ui

---

## Summary

A desktop content management app for post-kit. Provides a visual interface for creating content, managing posts, generating images, tracking analytics, and editing niche configuration — all powered by an AI adapter (Kiro CLI or similar) that runs the existing post-kit pipeline under the hood.

Single user. Local-first. Open source. No SaaS. No multi-user.

---

## Design Principles

1. **Filesystem is truth** — SQLite is a rebuildable index, never the source of truth
2. **Nothing hardcoded** — the app is a generic renderer of whatever the user's config defines
3. **PostKitBridge is the boundary** — the only code that reads/writes post-kit file structure
4. **Modular** — each feature owns its vertical (router + service + models), no cross-imports
5. **No over-engineering** — clean code, standard patterns, nothing clever for the sake of it
6. **Decoupled from niche** — removing `my-niche/` and replacing it with any niche must work with zero code changes

---

## Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Frontend | HTML + Tailwind CSS + Vanilla JS | Simple, no framework overhead, fast to iterate |
| Templating | Jinja2 (server-rendered) | Clean separation, reusable partials |
| Backend | FastAPI (Python) | Async, modular, well-documented, industry standard |
| Desktop | Tauri (Rust) | Lightweight native shell (~3-15MB), spawns FastAPI |
| Database | SQLite | Local, single-file, rebuildable from filesystem |
| AI Engine | Adapter pattern (Kiro CLI primary) | Swappable — no lock-in to any tool |
| Image Gen | MCP client | Connects to whatever image MCP server user configures |

---

## Project Structure

```
post-kit/
├── engine/                     # existing (NEVER touched by app code)
├── my-niche/                   # existing (read/written through bridge only)
├── posts/                      # existing (source of truth for post content)
├── app/
│   ├── backend/
│   │   ├── main.py             # FastAPI entry, mounts routers, startup events
│   │   ├── config.py           # App settings (paths, adapter, MCP servers)
│   │   ├── core/
│   │   │   ├── bridge.py       # PostKitBridge — reads/writes post-kit files
│   │   │   ├── database.py     # SQLite setup, migrations, rebuild logic
│   │   │   ├── events.py       # Event bus (pub/sub between modules)
│   │   │   └── models.py       # Shared base models (PostStatus enum, etc.)
│   │   ├── adapters/
│   │   │   ├── base.py         # Abstract AI adapter interface
│   │   │   ├── kiro.py         # Kiro CLI adapter
│   │   │   └── claude.py       # Claude Code adapter
│   │   ├── mcp/
│   │   │   ├── client.py       # MCP client (image generation, future)
│   │   │   └── registry.py     # Discovers available MCP servers from config
│   │   ├── modules/
│   │   │   ├── content/        # Content creation + scout + pipeline
│   │   │   │   ├── router.py
│   │   │   │   ├── service.py
│   │   │   │   └── models.py
│   │   │   ├── library/        # Posts library + editor + statuses + preview
│   │   │   │   ├── router.py
│   │   │   │   ├── service.py
│   │   │   │   └── models.py
│   │   │   ├── calendar/       # Queue + scheduling + cadence
│   │   │   │   ├── router.py
│   │   │   │   ├── service.py
│   │   │   │   └── models.py
│   │   │   ├── images/         # Image gen (MCP) + media library + carousel
│   │   │   │   ├── router.py
│   │   │   │   ├── service.py
│   │   │   │   └── models.py
│   │   │   ├── analytics/      # Dashboard + import/export
│   │   │   │   ├── router.py
│   │   │   │   ├── service.py
│   │   │   │   └── models.py
│   │   │   ├── credits/        # Plan + usage tracking
│   │   │   │   ├── router.py
│   │   │   │   ├── service.py
│   │   │   │   └── models.py
│   │   │   └── notifications/  # Activity feed + alerts
│   │   │       ├── router.py
│   │   │       ├── service.py
│   │   │       └── models.py
│   │   ├── brand/
│   │   │   ├── router.py       # Niche identity, voice, rules editing
│   │   │   └── service.py
│   │   └── onboarding/
│   │       ├── router.py       # First-run guided setup
│   │       └── service.py
│   ├── frontend/
│   │   ├── templates/
│   │   │   ├── base.html       # App shell (sidebar, topbar, command bar)
│   │   │   ├── onboarding.html
│   │   │   ├── content.html    # Content creation + scout tabs
│   │   │   ├── library.html    # Posts grid/list + inline editor
│   │   │   ├── calendar.html   # Calendar + queue view
│   │   │   ├── images.html     # Media library + generator + carousel
│   │   │   ├── analytics.html  # Charts + tables
│   │   │   ├── brand.html      # Identity, voice, rules editor
│   │   │   └── settings.html   # Adapter, paths, MCP config
│   │   ├── static/
│   │   │   ├── css/app.css     # Tailwind compiled output
│   │   │   ├── js/
│   │   │   │   ├── app.js      # Core (command bar, nav, fetch utils)
│   │   │   │   ├── editor.js   # Markdown editor + preview
│   │   │   │   ├── chat.js     # Content creation chat interface
│   │   │   │   └── calendar.js # Calendar interactions
│   │   │   └── assets/         # Icons, logos
│   │   ├── components/         # Reusable Jinja2 partials
│   │   │   ├── sidebar.html
│   │   │   ├── post-card.html
│   │   │   ├── chat-bubble.html
│   │   │   ├── notification.html
│   │   │   └── command-bar.html
│   │   └── tailwind.config.js
│   ├── tauri/
│   │   ├── src-tauri/
│   │   │   ├── src/main.rs     # Spawns FastAPI, opens webview
│   │   │   ├── tauri.conf.json
│   │   │   └── Cargo.toml
│   │   └── icons/
│   ├── data/                   # App-managed persistent data
│   │   ├── postkit.db          # SQLite (rebuildable)
│   │   ├── media/              # Uploaded/generated images
│   │   ├── imports/            # Raw CSV/Excel backup copies
│   │   └── config.json         # User preferences (adapter, theme, plan)
│   └── pyproject.toml          # Python deps
```

---

## Core Components

### PostKitBridge (`core/bridge.py`)

The single point of contact between the app and post-kit's file structure.

**Responsibilities:**
- Resolve post-kit root path (from config)
- Read `niche.yaml` → return parsed config (pillars, platforms, cadence, modules, etc.)
- Read any `my-niche/` file → return content
- Write to `my-niche/` files (for brand editing, onboarding)
- Resolve posts output path (from `niche.yaml → output.path` or defaults)
- Scan posts directory → return list of post folders with metadata
- Detect active modules (from `niche.yaml → modules_active`)
- Check VERSION vs postkit_version for update detection

**Rules:**
- No other code reads post-kit files directly — always through bridge
- Bridge never interprets content semantics (doesn't know what "pillars" mean for content)
- Bridge returns raw data — modules decide how to display it

### Adapter Interface (`adapters/base.py`)

Abstract interface that all AI tool adapters implement:

```python
class BaseAdapter:
    async def send_message(self, message: str, session_id: str = None) -> AsyncGenerator[str, None]:
        """Send a message, yield streaming response chunks.
        If session_id is provided, reuse an existing session (persistent conversation).
        If None, create a one-shot request-response."""
        ...

    async def start_session(self) -> str:
        """Start a persistent session (for multi-turn content creation). Returns session_id."""
        ...

    async def end_session(self, session_id: str) -> None:
        """Close a persistent session."""
        ...

    async def is_available(self) -> bool:
        """Check if the tool is reachable."""
        ...

    def get_name(self) -> str:
        """Return display name of the adapter."""
        ...
```

**How it works:**
- The adapter is initialized with the post-kit root path. It spawns the CLI tool pointed at that directory so AGENTS.md is auto-discovered and read by the AI tool.
- Commands are plain text messages (e.g., "what's trending", "write a post about X", "repurpose this for X"). The AI interprets them because it reads AGENTS.md — the app does no command routing.
- Content creation uses persistent sessions (multi-turn conversation). Scout and brainstorm use per-session as well. One-shot calls for simple queries.
- The app doesn't know how Kiro CLI or Claude Code work internally.

### MCP Client (`mcp/client.py`)

Connects to MCP servers for image generation and future integrations.

**Configuration:** Reads server configs from `app/data/config.json` using the same format as `.kiro/settings/mcp.json`:

```json
{
  "mcp_servers": {
    "image-gen": {
      "command": "uvx",
      "args": ["some-image-server@latest"],
      "env": {},
      "disabled": false
    }
  }
}
```

**Connection:** Spawns MCP server processes via stdio (or connects via SSE if configured). No authentication beyond what the individual MCP server requires.

**Registry (`mcp/registry.py`):** Discovers available servers from config, exposes their tools to modules that need them. If no MCP servers configured → image generation features are simply unavailable (no errors, feature just doesn't show).

Simple pub/sub for module-to-module communication:

```python
# Module A emits
events.emit("post.created", {"post_id": "...", "path": "..."})

# Module B listens
@events.on("post.created")
def update_index(data):
    ...
```

Events used for:
- Post created → library re-indexes
- Analytics imported → notifications fires
- Credits threshold hit → notifications fires
- Pipeline complete → notifications fires

No direct imports between modules. Ever.

### SQLite (`core/database.py`)

**What it stores:**
- Post index: path, title (first line), status, created date, published date, pillar (if in front-matter), platform (if in front-matter)
- Analytics: imported metrics (columns vary per import — stored as flexible key-value or JSON)
- Credits: usage counter, reset date
- Notifications: activity log

**Rebuild logic:**
1. On startup, if DB missing or `rebuild` flag set:
2. Scan `posts/` recursively → parse front-matter from each markdown file → build index
3. Scan `app/data/media/` → rebuild image metadata
4. Analytics: cannot rebuild (user re-imports from `app/data/imports/`)
5. Credits: reset to 0 (minor inconvenience)
6. Complete in seconds for typical post counts (<1000 posts)

---

## App Startup Sequence

```
1. Tauri launches → spawns FastAPI as child process
2. FastAPI reads app/data/config.json
   → Resolves post-kit root path
   → Selects active adapter
3. PostKitBridge scans:
   → Does my-niche/niche.yaml exist?
     → No: set app state to "needs_onboarding"
     → Yes: load config, resolve paths, detect modules
4. SQLite index check:
   → DB exists and not stale? → serve from index
   → DB missing or stale? → rebuild from filesystem
5. Version check:
   → Compare VERSION vs niche.yaml postkit_version
   → If behind → emit "update.available" event → notification created
6. Frontend loads in Tauri webview
   → If needs_onboarding → full-screen onboarding flow
   → Else → normal app shell with sidebar
```

---

## Post Lifecycle

Every post flows through these statuses:

```
idea → scouted → drafting → draft → in_review → approved → published → archived
```

| Status | Meaning | Trigger |
|--------|---------|---------|
| `idea` | Topic saved for later | User manual entry |
| `scouted` | AI found this as a candidate | Scout returns candidates |
| `drafting` | Pipeline actively generating | Pipeline triggered |
| `draft` | Pipeline complete, awaiting review | Pipeline finishes |
| `in_review` | User opened editor, making changes | User clicks edit |
| `approved` | Ready to publish, in queue | User approves |
| `published` | User posted it (manually) | User marks published |
| `archived` | Old/rejected, kept for reference | User archives |

**Storage:** Status tracked in SQLite index. Optionally written to post markdown front-matter:

```yaml
---
status: draft
created: 2026-07-29T14:00:00
pillar: <value from niche.yaml content_pillars>
platform: <value from niche.yaml platforms>
---
```

If front-matter is missing → default to `published` (backward compatible with existing posts).

**Front-matter ownership:** The app writes and manages front-matter. When the adapter creates a new post (plain markdown), the library service adds front-matter (status: draft, created: now, pillar/platform if inferable from the creation context). When the user changes status in the UI, the app updates front-matter in the file.

---

## Frontend Architecture

### App Shell (`base.html`)

- **Sidebar:** Always visible. Grouped navigation (Create / Manage / Insights / Settings). Credits widget always visible at bottom.
- **Top bar:** Page title + command bar (Cmd+K / Ctrl+K) + notification bell with unread count.
- **Main area:** Swaps content per page via Jinja2 template inheritance.

### Navigation (dynamic):

Sidebar items rendered conditionally based on config:

| Item | Condition to show |
|------|-------------------|
| Content | Always |
| Images | Active if image module enabled OR MCP image servers configured |
| Library | Always |
| Calendar | Always |
| Analytics | Active if analytics module enabled in niche.yaml |
| Brand | Always |
| Settings | Always |

If a module is not active → its nav item does not render.

### Command Bar:

- Triggered by Cmd+K / Ctrl+K
- Shows available actions built dynamically from active modules + registered routes
- Fuzzy search across actions
- Examples: "Scout for topics", "Write about...", "Import analytics", "Edit voice"

### Interactivity (Vanilla JS):

- `app.js` — command bar, navigation, shared fetch utilities, notification polling
- `chat.js` — content creation chat (send message, render streaming response)
- `editor.js` — markdown editing with live preview (split pane)
- `calendar.js` — month/week view rendering, drag-drop for queue

No framework. No virtual DOM. Direct DOM manipulation with fetch calls to FastAPI endpoints.

---

## Module Specifications

### Content Module

**Purpose:** Content creation — scout for topics + chat-based pipeline triggering.

**Pages:** `content.html` with two tabs: Scout | Create

**Scout tab:**
- "Scout now" button sends scout command to adapter
- Displays whatever candidates the adapter returns (rendered as cards)
- Fields shown depend on response (topic, source, angle, urgency — if present)
- User picks a candidate → "Draft this" triggers pipeline

**Create tab:**
- Chat interface — user types messages, sees streaming AI responses
- Pipeline progress shown as status messages (whatever the adapter returns)
- Final output saved to posts folder via bridge → event emitted → library indexes

**API endpoints:**
- `POST /api/content/scout` — trigger scouting
- `POST /api/content/create` — send message to adapter
- `GET /api/content/stream/{session_id}` — SSE stream for responses

---

### Library Module

**Purpose:** Browse, search, filter, edit, and manage all posts.

**Page:** `library.html` — grid/list view + inline editor

**List view:**
- Post cards showing: hook (first line), status badge, date, pillar (if defined), platform (if defined)
- Filters: status (always), date range (always), pillar (if content_pillars exists), platform (if multiple defined)
- Search: full-text across post content
- Sort: by date, status

**Editor (inline, opens on post click):**
- Split view: markdown editor (left) + rendered preview (right)
- Preview renders the post as it would appear (plain formatted text)
- If multiple platforms → toggle preview between them

**Actions per post:**
- Approve → status: approved, enters queue
- Archive → status: archived
- Repurpose → sends to adapter with repurpose command
- Regenerate → sends back to adapter with user notes
- Export → download as markdown or copy to clipboard

**API endpoints:**
- `GET /api/library/posts` — list with filters
- `GET /api/library/posts/{id}` — single post content
- `PUT /api/library/posts/{id}` — update content or status
- `DELETE /api/library/posts/{id}` — archive
- `GET /api/library/export` — export to CSV/Excel

---

### Calendar Module

**Purpose:** Visual scheduling and queue management.

**Page:** `calendar.html` — month/week grid + queue sidebar

**Calendar view:**
- Displays posts on their dates (from index)
- Reads cadence from niche.yaml:
  - `posts_per_day` → visualize max slots per day
  - `best_days` → highlighted cells
  - `slow_days` → dimmed cells
  - If cadence not defined → neutral grid, no highlights
- Posts color-coded by status (draft, approved, published)

**Queue sidebar:**
- Lists approved posts not yet scheduled/published
- Drag-and-drop onto calendar dates
- Warns only if user-defined cadence rules would be violated

**API endpoints:**
- `GET /api/calendar/month/{year}/{month}` — posts for a month
- `PUT /api/calendar/schedule/{post_id}` — assign date to post

---

### Images Module

**Purpose:** Image generation via MCP + upload/paste media library + carousel builder.

**Page:** `images.html` — three views: Library | Generate | Carousel

**Library view:**
- Grid of all images in `app/data/media/`
- Filter by date, tags
- Click to preview, copy path, or attach to a post

**Generate view:**
- Prompt input → sends to MCP client → result saved to media folder
- Can also select a post and generate based on it (sends post content + "generate image" to adapter)

**Carousel builder:**
- Add/remove slides, edit text per slide, reorder via drag-drop
- Outputs markdown structure matching carousel module format
- Visual preview of slide sequence

**Media storage:**
- Files saved to `app/data/media/` with timestamp-based naming
- Metadata stored in JSON manifest (`app/data/media/manifest.json`)
- Manifest includes: filename, created date, tags, associated post (if any)

**API endpoints:**
- `GET /api/images/list` — media library
- `POST /api/images/upload` — upload/paste
- `POST /api/images/generate` — send prompt to MCP
- `GET /api/images/carousel/{post_id}` — carousel data
- `PUT /api/images/carousel/{post_id}` — save carousel

---

### Analytics Module

**Purpose:** Performance tracking with CSV/Excel import and data visualization.

**Page:** `analytics.html` — import + dashboard views

**Import flow:**
- Upload CSV/Excel file
- App parses whatever columns exist (no assumed column names)
- User maps columns to display fields (date, metric name, value)
- Raw file saved to `app/data/imports/` as backup
- Parsed data stored in SQLite

**Dashboard:**
- Charts and tables from imported data
- Grouped by whatever dimensions exist in user's config:
  - By pillar (if content_pillars defined)
  - By platform (if multiple platforms)
  - By date range (always)
  - By any other dimension the imported data provides
- No hardcoded metric names — renders whatever columns were imported

**Export:**
- Any view exportable to CSV/Excel
- Full post library with metadata exportable

**API endpoints:**
- `POST /api/analytics/import` — upload and parse file
- `GET /api/analytics/dashboard` — aggregated data for charts
- `GET /api/analytics/export` — download data

---

### Credits Module

**Purpose:** Display plan name and usage tracking.

**Display:** Always visible in sidebar — plan name + usage bar + count.

**Data:**
- Stored in `app/data/config.json`:
  ```json
  {
    "plan": { "name": "Free", "limit": 100, "period": "monthly" },
    "usage": { "count": 42, "reset_date": "2026-08-01" }
  }
  ```
- Incremented when adapter is called (any pipeline/scout/brainstorm call)
- Resets based on period (monthly by default)

**API endpoints:**
- `GET /api/credits` — current plan + usage
- `PUT /api/credits/plan` — update plan info

---

### Notifications Module

**Purpose:** Activity feed and alerts.

**Display:** Bell icon in topbar + dropdown list.

**Sources (event-driven):**
- `post.created` → "Post ready for review"
- `update.available` → "post-kit update available"
- `credits.threshold` → "Approaching usage limit"
- `analytics.imported` → "Analytics imported successfully"
- Any adapter response flagged as urgent → surfaced

**Storage:** SQLite table (id, type, message, read status, timestamp, link).

**API endpoints:**
- `GET /api/notifications` — list (unread first)
- `PUT /api/notifications/{id}/read` — mark as read
- `GET /api/notifications/unread-count` — for badge

---

### Brand Section

**Purpose:** View and edit niche identity files.

**Page:** `brand.html` — list of niche files with editors.

**Behavior:**
- Scans `my-niche/` directory via bridge
- Lists whatever files exist (not a hardcoded list)
- Each file shows: filename + content summary + "Edit" button + "Improve with AI" button
- Edit: opens file content in markdown/yaml editor, saves via bridge
- Improve with AI: sends to adapter for brainstorm flow (user confirms changes before save)
- Files that don't exist don't appear — no empty placeholders

**API endpoints:**
- `GET /api/brand/files` — list all niche files
- `GET /api/brand/files/{filename}` — file content
- `PUT /api/brand/files/{filename}` — save edited file
- `POST /api/brand/improve/{filename}` — send to adapter for suggestions

---

### Settings

**Purpose:** Technical configuration only. Does not handle niche content.

**Page:** `settings.html`

**Sections:**
- Adapter selection (Kiro CLI, Claude Code, etc.)
- Post-kit directory path
- MCP server configuration (servers for image gen, future integrations)
- Version status (current VERSION vs postkit_version — shows notice, "Update" button redirects to Brand where adapter walks through changes per-file)
- Theme preference (dark/light)
- Rebuild index button (manual trigger for SQLite rebuild)

**Boundary:** Settings owns technical config (paths, adapter, MCP, theme, index). Brand owns all niche file operations, including applying updates to niche files.

**API endpoints:**
- `GET /api/settings` — current config
- `PUT /api/settings` — update config
- `POST /api/settings/rebuild` — trigger index rebuild

---

### Onboarding

**Purpose:** First-run setup when `my-niche/niche.yaml` doesn't exist.

**Page:** `onboarding.html` — full-screen, no sidebar.

**Flow:**
1. App detects missing niche.yaml
2. Full-screen onboarding page loads
3. Sends guided setup command to adapter
4. AI asks questions one at a time → displayed as chat messages
5. User answers in chat interface
6. After all questions → adapter generates `my-niche/` files
7. Bridge detects new files → app reloads with full sidebar active

No hardcoded questions in the app — the adapter reads `engine/core/onboarding.md` and handles it.

---

## Data Storage Summary

| Data | Location | Rebuildable? |
|------|----------|-------------|
| Posts (content) | `posts/` filesystem | Source of truth — never lost |
| Niche config | `my-niche/` filesystem | Source of truth — never lost |
| Post index | SQLite | Yes — rebuild from filesystem scan |
| Analytics | SQLite | Partially — re-import from `app/data/imports/` |
| Images | `app/data/media/` filesystem | Files always exist, manifest rebuildable |
| Credits/usage | `app/data/config.json` | Reset to 0 (minor) |
| Notifications | SQLite | Lost on rebuild (acceptable) |
| Import backups | `app/data/imports/` filesystem | Always preserved |
| App config | `app/data/config.json` | User re-configures (one-time) |

---

## Dependencies (Python)

```
fastapi
uvicorn
jinja2
python-multipart    # file uploads
openpyxl            # Excel import/export
aiosqlite           # async SQLite
pyyaml              # niche.yaml parsing
markdown            # preview rendering
```

---

## What This App Does NOT Do

- Auto-publish to any platform (no API integrations — user posts manually)
- Know anything about content strategy, hooks, voice, or quality
- Contain any niche-specific logic
- Require internet access to function (except when adapter calls AI or MCP generates images)
- Run as a server for others (single user, local only)
- Replace post-kit's engine — it's a UI layer on top of it

---

## Hard Problems & Decisions

### Adapter Process Management

The adapter spawns a CLI tool (e.g., `kiro-cli chat`) as a long-running child process:

- **Spawning:** Process started with the post-kit root as working directory. stdin/stdout piped.
- **Message boundaries:** The adapter reads line-by-line and uses a delimiter or EOF-per-response pattern. Implementation will need to experiment with each CLI tool's output format and define a parsing strategy per adapter.
- **Session lifecycle:** One process per session. `start_session()` spawns process, `send_message()` writes to stdin, yields from stdout. `end_session()` sends exit/quit command and terminates process.
- **Error recovery:** If process dies mid-session → adapter emits error event → UI shows "Session lost, retry?" → user can restart. No automatic retry (AI calls are expensive).
- **Timeouts:** Configurable per-adapter (default 120s for generation, 30s for scout). Timeout → kill process → show error.

### Scout Output Rendering

The scout tab renders AI output as **rich markdown** — not structured cards. The adapter returns text (markdown tables, lists), and the UI renders it using the markdown library. The user interacts via the chat interface ("draft #3", "tell me more about #5"). No parsing of AI output into structured data — that's fragile and breaks when AI format changes.

If in the future we want true structured output, the adapter interface can be extended with a `send_structured_request()` method that asks the AI to respond in JSON. But v1 is text-in, text-out.

### Tauri ↔ FastAPI Coordination

- **Port:** FastAPI starts on a random available port (OS assigns). Writes port to a temp file.
- **Readiness:** Tauri polls the health endpoint (`GET /api/health`) until it returns 200, then loads the webview URL.
- **Crash recovery:** Tauri monitors FastAPI process. If it dies → shows "Backend crashed, restarting..." → respawns.
- **URL:** Webview points to `http://localhost:{port}` read from the temp file.

### Staleness Detection

On startup, compare:
- `last_index_build` timestamp (stored in SQLite metadata table)
- Most recent file modification time across `posts/` directory tree

If any file in posts/ is newer than last_index_build → rebuild. If posts/ folder doesn't exist yet → index is empty (valid state). This is a single filesystem stat call per startup — fast.

During runtime: no file watcher. After any adapter session that involves content creation, library service rescans posts/ for new/modified files since session start (timestamp comparison). Simple, no daemon needed.

### Post Detection After Generation

After an adapter session ends (content creation, repurpose, etc.):
1. Library service records a "session start" timestamp before adapter call
2. After adapter finishes, scans posts/ for files with mtime > session start
3. New files found → indexed, status set to "draft", event emitted
4. No file watcher, no convention with adapter — just filesystem timestamps

### Error Handling & Offline Behavior

| Scenario | Behavior |
|----------|----------|
| Adapter unavailable (CLI not installed) | App works in read-only mode. Library, calendar, analytics, brand editing all function. Content creation shows "Adapter not available — check Settings" |
| Adapter authenticated but network fails mid-generation | Stream stops → timeout fires → "Generation failed, try again?" |
| MCP server not configured | Image generation features hidden (nav item doesn't render) |
| MCP server configured but fails to connect | "Image generation unavailable" message in Images module. Rest of app unaffected |
| SQLite corrupt | Auto-detected on startup → deleted → rebuilt from filesystem |
| posts/ folder empty or missing | Valid state. Library shows empty, calendar shows empty. No errors |

### Event Bus Simplicity

The event bus is the observer pattern in < 50 lines. Synchronous, in-process, no async queues, no message brokers. It's a dict of event_name → list of callback functions. `emit()` calls each synchronously. If a listener fails, it logs and continues. That's it.

If contributors find the indirection confusing during early development, the event bus can be replaced with direct function calls and refactored back in later. It's a convenience, not load-bearing architecture.

### Chat Component Reuse

The chat UI (chat-bubble component + message list + input field + streaming handler) is a reusable Jinja2 partial + JS module. Used in:
- Content/Create tab (main content creation)
- Onboarding (guided setup)
- Brand "Improve with AI" (opens inline chat panel on that page)

Same component, different contexts. No duplication.

---

## Future Extensibility

Adding a new feature:
1. Create `app/backend/modules/new_feature/` with router.py, service.py, models.py
2. Mount router in main.py
3. Create `frontend/templates/new_feature.html`
4. Add nav item to sidebar (conditional on config if module-dependent)
5. Done — no existing code modified

Adding a new adapter:
1. Create `app/backend/adapters/new_tool.py` implementing BaseAdapter
2. Register in config as an option
3. Done — app works the same with new tool

Adding a new MCP integration:
1. Configure MCP server in settings
2. MCP client auto-discovers it via registry
3. Modules that use MCP can now access new capabilities

---

## Implementation Phasing (Suggested)

This spec is too large for a single implementation pass. Suggested phases:

**Phase 1 — Core (functional app):**
- Tauri shell + FastAPI bootstrap
- PostKitBridge + config
- SQLite with rebuild logic
- Library module (browse, filter, status management, editor)
- Content module (chat + scout)
- Adapter (Kiro CLI)
- App shell (sidebar, topbar, command bar)
- Onboarding flow

**Phase 2 — Visual + Planning:**
- Calendar module (queue, scheduling, cadence)
- Images module (MCP client, media library, upload, carousel)
- Brand section (niche file editing)

**Phase 3 — Insights + Polish:**
- Analytics module (CSV import, dashboard, export)
- Credits module (plan display, usage tracking)
- Notifications module (activity feed, alerts)
- Settings page (full config management)

Each phase produces a usable app. Phase 1 alone covers the primary workflow (create content + manage posts).
