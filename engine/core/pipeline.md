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

**Runs immediately after receiving a content request — before any research or web search.**

1. Identify the topic/slug the user is asking about.
2. Scan `posts/` for the current month's folder.
3. If a post with a similar slug or overlapping topic already exists, **stop and inform the user** before doing anything else:
   - List the existing post(s) that overlap.
   - Ask: proceed anyway, find a fresh angle, or pick a different topic?
4. Only continue to Step 1 (Research) if the user confirms or no duplicate is found.

**Why this runs first:** Web search and research cost time and tokens. Don't spend either on a topic that's already been covered unless the user explicitly wants a new angle.

---

## Step 1: Research

**Skip if:** the user provides a specific topic with enough context, or news-scout module is not active.

**Run if:** user says "what's trending", "find me something to post about", or the topic needs current data.

**If the user asks "what's trending" / "find me topics" / "what should I post about":** run **The Daily Scout Command** defined in `my-niche/news-scout.md` — follow the candidate composition and presentation rules defined there, then let the user pick which to write.

**How to research — follow `engine/core/web-research.md`:**

The web-research module handles all search strategy. It will:
1. Classify the research intent (quick fact vs deep investigation)
2. Run multi-angle searches (direct + community + authoritative)
3. Triage sources by quality, recency, and cross-validation
4. Fetch and extract key passages from top sources
5. Synthesize findings into content-ready format (what happened → why it matters → the angle)

**Additional source checks:**
- Check the user's `sources.md` for where to look (subreddits, feeds, communities)
- Cross-validate: a topic is worth posting about if it appears in 2+ independent sources
- Score urgency:
   - Happening right now → post today
   - Trending this week → post within 2-3 days
   - Evergreen → queue for whenever

Present research findings to the user. Let them pick or direct you.

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

1. Create the output folder: `posts/YYYY-month/YYYY-MM-DD-slug/`
   - **No subfolders** inside the month folder (no `daily/`, `news/`, `github/`)
   - Every post goes flat inside the month, identified by its date-slug folder
   - Example: `posts/2026-july/2026-07-14-slug/linkedin-post.md`
2. Save the post as `linkedin-post.md` (or `x-post.md` if platform-specific)
3. If image-prompts module is active, include 3 AI image prompts in the post file
4. If github-screenshot module is active and this is a repo post, capture/provide screenshot
5. Present the final post to the user for approval

---

---

## Platform Adaptation

If the user has multiple platforms active, ask:
> "Want me to write this for LinkedIn only, or adapt it for [other active platforms] too?"

If adapting for multiple platforms, run Steps 2-5 once per platform, following each platform's specific rules from `engine/platforms/`.
