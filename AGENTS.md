# post-kit

A zero-code content creation pipeline for any niche. Research, write, and polish posts that sound like you — for any platform.

## How This Works

This project is a set of markdown instruction files that you (the AI agent) read and follow to help users create content.

## First Run

Check if `my-niche/niche.yaml` exists.

- **If it doesn't exist:** Read and follow `engine/core/onboarding.md` to set up the user's pipeline.
- **If it exists:** The user is set up. Follow the pipeline for any content request.

## Pipeline

For every content request, follow `engine/core/pipeline.md`:

```
Dedup Check (FIRST — before anything else) → Research → Write → Voice Pass → Anti-AI Pass → Quality Gate → Output
```

### ⛔ CRITICAL: Dedup runs BEFORE research
The very first action for ANY content request (including "what's trending") is:
1. Read `my-niche/niche.yaml` → resolve output path (`output.path`, defaults to `../posts`)
2. LIST the current month's posts folder (e.g., `posts/2026-july/`) — actually list it, get all folder names
3. Load that list into context

**Do NOT run any web search or fetch any URL until you have completed step 2 above.** This is a hard gate.

### Files to read before writing any content:
1. `my-niche/niche.yaml` — user's identity and pillars
2. `my-niche/voice.md` — how they sound
3. `my-niche/content-rules.md` — structure, length, hooks
4. Active platform file from `engine/platforms/` (linkedin.md is default)
5. `engine/core/anti-ai-writing.md` — mandatory pass (never skip)
6. `engine/core/quality-gates.md` — every post must pass

### Optional modules (only active if the file exists in `my-niche/`):
- `visual-system.md` — image approach
- `memes.md` — humor pipeline
- `news-scout.md` — trending topic discovery
- `video-content.md` — video creation
- `image-prompts.md` — AI image prompts
- `analytics.md` — performance tracking
- `repurpose.md` — multi-platform adaptation
- `carousel.md` — slide content

## Commands the User Might Say

| User says | What to do |
|-----------|-----------|
| "write a post about [topic]" | Run the full pipeline |
| "what's trending" / "find me topics" / "what should I post about" | Use news-scout module → run "The Daily Scout Command" from `my-niche/news-scout.md` |
| "roast [topic]" / "meme about [x]" | Use memes module (if active) |
| "help me improve my [voice/hooks/etc]" | Follow `engine/core/brainstorm.md` |
| "humanize this" | Run anti-AI pass from `engine/core/anti-ai-writing.md` |
| "repurpose this for X" | Use repurpose module (if active) |
| "make a video" / "video about [x]" | Use video-content module (if active) |
| "update my niche" / "check for updates" / "what changed in post-kit" | Follow `engine/core/update.md` — reconcile niche with latest post-kit improvements |

## Output

Save posts to: `posts/YYYY-month/YYYY-MM-DD-slug/linkedin-post.md`

**This is the only valid path structure.** No subfolders like `daily/`, `news/`, `github/` inside the month folder. Every post goes flat inside the month, identified only by its date-slug folder.

Example: `posts/2026-july/2026-07-14-australia-ai-copyright/linkedin-post.md`

## Key Rules

- ALWAYS run the anti-AI pass. No exceptions.
- ALWAYS check quality gates before delivering a post.
- NEVER write a post without reading the user's voice.md first.
- If a module file doesn't exist in `my-niche/`, that feature is not active — don't suggest it.
- The user can change anything anytime by editing files or asking you to help via the brainstorm skill.
