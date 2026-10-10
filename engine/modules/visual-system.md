# Visual System Module

Handles how visuals (images, screenshots, graphics) are selected and used for posts.

---

## When This Module is Active

Every post gets a visual recommendation. The AI decides what type of visual fits the content and either provides it or tells the user what to create.

---

## Visual Selection Priority

**Real media beats generated media every time it exists.** A real screenshot is specific by definition and can't look AI-averaged. A generated image has to earn its specificity through a tight brief. Choose in this order (first match wins):

1. **Real screenshot** of the actual thing being discussed (product, pricing page, UI, tweet, repo)
2. **Sourced image** from relevant communities (for memes/reactions)
3. **Stock photo/video** from free sources (Pexels, Unsplash, Pixabay)
4. **Simple text card** (named dark background + readable text, for data or quotes)
5. **AI-generated image** (LAST RESORT — provide prompts for the user that pass the slop check in `image-prompts.md`)
6. **No image** — if the post is pure opinion/text and works better without one

When you reach step 4 or 5, the prompt must pass the image-prompts slop check: no vibe adjectives, a named exact background, the specific detail baked in, exact text quoted. A vague prompt averages into the generic AI-image look.

---

## Post Nature → Visual Approach

Match the content type to the right visual:

| Content Type | Visual Approach |
|-------------|----------------|
| Pricing, cost, money | Screenshot of pricing page OR data card |
| Data, benchmarks, stats | Dark UI data card with real numbers |
| Company news, drama | Real photo + text overlay |
| Comparison, "vs" | Split panel with logos/stats |
| Humor, irony | Source real meme OR generate absurdist scene |
| Jobs, layoffs, career | Stock photo + bold text overlay |
| Funding, business deals | Simple text card on dark background |
| Code, repos, tools | Screenshot of actual repo/code |
| Opinion, hot take | NO image — plain text wins |
| Tutorial, how-to | Step-by-step screenshots or diagram |
| Personal story | No image, or a candid/contextual photo |

---

## Image Specs

Set these based on your platform:

| Platform | Format | Size |
|----------|--------|------|
| LinkedIn feed | 4:5 portrait | 1080x1350 |
| LinkedIn data cards | 1:1 square | 1080x1080 |
| X (Twitter) | 16:9 landscape | 1200x675 |
| Instagram | 1:1 square | 1080x1080 |
| Instagram story | 9:16 vertical | 1080x1920 |

---

## Responsibilities

**AI handles:**
- Suggesting which visual type to use
- Finding stock photos/videos via web search
- Creating text cards (describe the card for the user)
- Taking screenshots (if tool available)
- Downloading free stock assets

**User handles:**
- AI image generation from prompts the AI provides
- Uploading personal photos
- Screenshots of their own tools/products

---

## Post Output Format

Every post with a visual should include:

```markdown
## Visual
**Type:** [Screenshot / Stock / Text card / AI-generated / None]
**Description:** [What the visual shows]
**Status:** [Ready / User needs to create]
```

If AI-generated, provide the prompt for the user — and make sure it passes the slop check in `image-prompts.md` (no vibe adjectives, named background, specific detail baked in, exact text quoted).

---

## When to Skip Visuals

- Pure opinion posts (text-only often outperforms)
- Very short posts (1-4 lines) that are the hook themselves
- When the user explicitly says "no image for this one"
- When no visual would add value beyond decoration
