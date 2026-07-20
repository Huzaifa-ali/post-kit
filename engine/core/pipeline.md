# Pipeline

The universal content creation flow. Every post goes through these steps in order.

---

## Version Check (runs once per session)

Before the first content request in a session, check if the user's niche is behind the current post-kit version:

1. Read the `VERSION` file at the project root.
2. Read `my-niche/niche.yaml` and check the `postkit_version` field.
3. If `postkit_version` is missing or is lower than `VERSION`, display a **single, non-blocking notice**:

> "post-kit updated to [VERSION] — your niche is on [user version]. Say **'update my niche'** to review what's new (optional, nothing changes without your approval)."

4. Then proceed normally with the content request. Never block the user's workflow for an update.
5. Do NOT repeat this notice after the first content request in a session — once per session is enough.

---

## Flow

```
Request → Dedup Check → Research → Write → Voice Pass → Anti-AI Pass → Quality Gate → Output
```

---

## Step 0: Dedup Check

**Runs for every content request — before any research or writing.**

### What to do:

1. **Find the user's posts folder.** Read `my-niche/niche.yaml` and check for an `output` field:
   - If `output.path` is defined, use that as the posts root folder (e.g., `content/linkedin/`)
   - If no `output` field exists, default to `posts/`
   - The folder naming follows `output.structure` if set, otherwise defaults to `YYYY-month/YYYY-MM-DD-slug/`

2. **List the current month's post folders.** Get all folder names for this month. Keep this list in context for the rest of the pipeline.

3. **If the user gave a specific topic:** check the list now. A post is a DUPLICATE only if it covers the **same subject AND same angle**. It is NOT a duplicate if:
   - Same broad category but different subject (e.g., two different tools, two different people)
   - Same subject but different angle (e.g., "tool-X-launch" vs "tool-X-pricing-change" vs "tool-X-tutorial")
   - Same topic area but different news/event
   - A follow-up or new development on a prior story
   
   If duplicate found → stop and inform the user. Ask: proceed anyway, find a fresh angle, or pick a different topic?

4. **If the user is scouting** ("what's trending", "what's new today", etc.): proceed to Step 1 with the existing posts list loaded. Use it to filter out already-covered topics from scout results before presenting candidates.

### Important:
- This check uses folder names only — do NOT read every post file. Slug-based matching is sufficient.
- When in doubt (borderline overlap), proceed and note it briefly rather than blocking the user.
- This check prevents self-repetition within the same month.

---

## Step 1: Research

**This step ALWAYS runs unless the user provides a complete, self-contained topic with all facts included.**

### When to SKIP research:
- User pastes a full article/link and says "write about this" (they've done the research)
- User provides specific facts, numbers, and context in their request
- The topic is purely opinion-based and needs no external data

### When to RUN research (default — if in doubt, research):
- User gives a topic name without full context (e.g., "write about [topic]")
- User says "what's trending", "find me something to post about", "what's new today"
- Topic involves current events, numbers, dates, or claims that need verification
- News-based content — always verify freshness and accuracy before writing

### How to research:

**Follow `engine/core/web-research.md` for the full search strategy.** The key steps:

1. **Actually run web searches.** Do not skip this. Use the search tool to query for the topic.
2. Classify the research intent (quick fact vs deep investigation)
3. Run multi-angle searches (direct + community + authoritative)
4. Triage sources by quality, recency, and cross-validation
5. Fetch and extract key passages from top sources
6. Synthesize findings into content-ready format (what happened → why it matters → the angle)

### If the user asks "what's trending" / "find me topics" / "what should I post about":
Run **The Daily Scout Command** defined in `my-niche/news-scout.md` — follow the candidate composition and presentation rules defined there, then let the user pick which to write.

### Additional source checks:
- Check the user's `sources.md` for where to look (subreddits, feeds, communities)
- Cross-validate: a topic is worth posting about if it appears in 2+ independent sources
- Score urgency:
   - Happening right now → post today
   - Trending this week → post within 2-3 days
   - Evergreen → queue for whenever

### After research:
- If the user gave a specific topic: proceed directly to Step 2 (Write) with the researched facts
- If scouting/exploring: filter candidates against the existing posts list from Step 0, present only fresh topics, let user pick → proceed to Step 2

---

## Step 2: Write

Read these files before drafting:
- `my-niche/niche.yaml` — their identity and content pillars
- `my-niche/content-rules.md` — post structure, length, hooks
- Active platform file from `engine/platforms/` — format constraints

Then draft the post following the structure defined in their content-rules.

### Writing principles:
- One idea per post
- Hook in the first 1-2 lines (the "see more" gate on most platforms)
- Short sentences, short paragraphs
- Include one genuine personal opinion
- End with a CTA that invites disagreement or experience-sharing
- Match the length rules from content-rules.md

---

## Step 3: Voice Pass

Read `my-niche/voice.md` and rewrite the draft to match their voice profile.

Check:
- Does this sound like THEM, not generic AI?
- Are the voice rules being followed? (tone, banned phrases, personality)
- Would they actually say this out loud?

If it doesn't pass, rewrite until it does.

---

## Step 4: Anti-AI Pass (Mandatory)

Read `engine/core/anti-ai-writing.md` and run the full check.

This step is ALWAYS active. It cannot be disabled. Every post must pass.

- Remove banned words
- Remove banned patterns
- Check for AI-sounding structure
- Make it sound human

---

## Step 5: Quality Gate

Read `engine/core/quality-gates.md` and evaluate the post.

The post must pass ALL gates to be published. If it fails any gate, revise and re-run from Step 3.

---

## Step 6: Output

1. **Use the same output path resolved in Step 0 (Dedup Check).** The posts root and folder structure were already determined from `my-niche/niche.yaml` at the start of the pipeline. Default: `posts/YYYY-month/YYYY-MM-DD-slug/`.
2. Create the output folder following that structure.
   - **No extra subfolders** inside the month folder (no `daily/`, `news/`, `github/`)
   - Every post goes flat inside the month, identified by its date-slug folder
3. Save the post as `linkedin-post.md` (or `x-post.md` if platform-specific)
4. If image-prompts module is active, include 3 AI image prompts in the post file
5. If github-screenshot module is active and this is a repo post, capture/provide screenshot
6. Present the final post to the user for approval

---

---

## Platform Adaptation

If the user has multiple platforms active, ask:
> "Want me to write this for LinkedIn only, or adapt it for [other active platforms] too?"

If adapting for multiple platforms, run Steps 2-5 once per platform, following each platform's specific rules from `engine/platforms/`.
