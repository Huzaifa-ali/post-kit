# Repurpose Module

Turn one piece of content into multiple platform-adapted versions. Write once, post everywhere — adapted, not copy-pasted.

---

## When to Repurpose

- After writing a strong post for your primary platform
- When the user says "turn this into an X post too" or "repurpose this"
- When multiple platforms are active and the content fits both

---

## Repurposing Flow

```
1. Take the original post
2. Identify the core message (one sentence)
3. For each target platform, rewrite following that platform's rules
4. Run Voice Pass on each version
5. Run Anti-AI Pass (all five layers) on each version
6. Output all versions
```

**Repurposing is where specifics get flattened into slop.** When you compress a LinkedIn post to an X post, the lazy move is to replace the concrete claim with a vague summary — "AI pricing is getting out of control" instead of "$544 vs $4,811, same task." Don't. Carry the specific numbers and names into every version. A shorter post is not a vaguer post. Each repurposed version must independently pass the generic test and the specificity gate — adaptation never strips the detail that made the original land.

---

## Adaptation Rules (Not Copy-Paste)

Each platform has different rules. Repurposing means ADAPTING, not just reformatting:

| From → To | What Changes |
|-----------|-------------|
| LinkedIn → X | Shorter. Punchier. Remove professional framing. Add thread if needed. |
| LinkedIn → YouTube | Add visual storytelling. Make it watchable, not just readable. |
| LinkedIn → Newsletter | Add context. Expand examples. More personal, less performative. |
| LinkedIn → Blog | Expand significantly. Add sections, depth, examples, data. |
| X → LinkedIn | Add context. Lengthen. More structured. Professional but not boring. |
| Blog → LinkedIn | Extract the key insight. Compress to post length. Link to full article. |
| Blog → X | Extract 3-5 punchiest lines. Thread or single tweet. |

---

## Platform-Specific Adaptation

Read the relevant platform file from `engine/platforms/` for each target. Key differences:

**LinkedIn:** Professional context, longer form, CTA at end, hashtags below fold
**X:** Ultra-short, hooks immediately, threads for longer content, engagement-bait works differently
**YouTube Community:** Visual-first, question-driven, polls
**Newsletter:** Personal, depth, exclusive angle, links okay in body
**Blog:** SEO-aware, structured with headings, comprehensive, evergreen

---

## What Makes a Post Repurposable

Not every post should be repurposed. Good candidates:
- Strong universal message (not platform-specific)
- High engagement on original (proven it resonates)
- Contains data, frameworks, or insights with lasting value
- Can be expanded OR compressed without losing the point

Bad candidates:
- Platform-specific format (LinkedIn carousel → X doesn't translate)
- Time-sensitive news (by the time you repurpose, it's old)
- Memes (humor rarely translates across platforms the same way)
- Very personal stories (may only fit one platform's audience)

---

## Output Format

When repurposing, output each version in its own file:

```
posts/YYYY-month/YYYY-MM-DD-slug/
├── linkedin-post.md
├── x-post.md
└── newsletter-post.md (if applicable)
```

Or present all versions in one response for the user to review.

---

## The User Decides

Always ask before repurposing:
> "This post would work well on [platforms]. Want me to adapt it?"

Never auto-repurpose without asking. The user might want to customize the timing or angle for each platform.
