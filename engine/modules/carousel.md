# Carousel Module

Handles multi-slide/carousel content for platforms that support it (LinkedIn, Instagram).

---

## When to Use Carousels

Carousels work best for:
- Step-by-step processes (how to do X in N steps)
- Lists/frameworks (5 things every [role] should know)
- Comparisons (before/after, old way/new way)
- Data breakdowns (stats with context per slide)
- Mini-tutorials (one concept per slide)

Don't use carousels for:
- Hot takes (just write the opinion as text)
- News reactions (screenshot + caption is faster)
- Personal stories (text-only is more intimate)
- Anything that can be said in 1-2 paragraphs

---

## Carousel Structure

### Cover Slide (Slide 1)
- HOOK — the reason to swipe
- Bold, specific headline
- Subheadline optional
- Must create curiosity: "what are the 5 things?"

### Body Slides (Slides 2-8)
- ONE point per slide
- Maximum 30-40 words per slide
- Visual hierarchy: headline → supporting text
- Consistent layout across all body slides
- Use numbers/bullets for scannability

### Closing Slide (Last Slide)
- CTA: follow, save, share, comment
- Summary of key point
- Or a question that drives engagement

---

## Carousel Specs

| Platform | Slides | Format | Size |
|----------|--------|--------|------|
| LinkedIn | 2-20 (sweet spot: 6-10) | PDF or images | 1080x1350 (4:5) |
| Instagram | 2-10 | Images | 1080x1080 or 1080x1350 |

---

## Design Principles

- **Consistent branding** across all slides (same fonts, colors, layout)
- **Readable on mobile** — large text, high contrast
- **One idea per slide** — if you need two paragraphs, split into two slides
- **Visual breathing room** — don't cram, use whitespace
- **Progress indicator** — slide numbers or dots help

---

## Text Rules for Slides

- Headlines: 5-8 words, bold
- Body text: 15-30 words max per slide
- Font size: minimum equivalent of 24pt (readable without zooming)
- Contrast: dark text on light bg OR light text on dark bg — never low contrast

---

## Anti-Slop for Carousels

Carousels are a slop magnet — the "5 things nobody told you about X" format invites filler, triads, and puffery. Every slide must earn its place.

- **Each slide carries a specific fact, not a vibe.** A slide that says "Consistency is key" or "Quality matters" is a wasted slide. Replace it with the number, the name, the concrete example. Slide-level generic test: if the slide's text could appear in a carousel about a different topic, it's filler — cut it or make it specific.
- **No manufactured round numbers.** Don't pad to "7 things" when you have 4 real ones. Four strong slides beat seven with filler. The count follows the content, not a headline template.
- **Cover slide: a specific hook, not a formula.** "5 things nobody told you about [X]" is the single most overused AI-carousel opener. Lead with the surprising number or the real claim instead ("Claude costs 9x more than DeepSeek for the same task").
- **Kill the puffery headlines.** "A game-changer", "the ultimate guide", "everything you need to know" — delete. State what the slide actually shows.
- **Closing slide: no empty CTA.** "Follow for more!" on every carousel is noise. Earn the follow with the content; make the CTA specific to this carousel's topic when you use one.
- **Visual slop applies too.** If slides are AI-generated, each prompt passes the `image-prompts.md` slop check (named background, no vibe adjectives, exact text quoted, specific detail baked in). Consistent layout across slides, but not the default AI-gradient look.

---

## Output Format

When creating carousel content, output:

```markdown
## Carousel
**Platform:** [LinkedIn / Instagram]
**Slides:** [number]
**Topic:** [one-line summary]

### Slide 1 (Cover)
**Headline:** [hook text]
**Subheadline:** [optional]

### Slide 2
**Headline:** [point 1]
**Body:** [supporting text]

### Slide 3
**Headline:** [point 2]
**Body:** [supporting text]

[...continue for all slides...]

### Slide [N] (Closing)
**CTA:** [call to action]

---
**Caption for post:**
[The text that accompanies the carousel in the feed]
```

---

## Carousel + Post

The carousel needs a caption (the actual post text). This should:
- Hook readers who see the post in feed
- Give context for why they should swipe
- Include the CTA
- Follow all normal post rules (voice, anti-AI, quality gates)
