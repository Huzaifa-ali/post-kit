# Video Content Module

Handles short-form video creation for social media posts.

---

## When to Use Video

- Meme clips (reaction videos, scene overlays)
- Quick demos or screen recordings
- Text-overlay storytelling on stock footage
- Before/after transformations
- Data visualization with motion

---

## Video Specs

| Platform | Format | Duration | Notes |
|----------|--------|----------|-------|
| LinkedIn | 9:16 vertical or 1:1 | 15-60 seconds | Auto-plays muted, text overlay required |
| X (Twitter) | 16:9 or 1:1 | 15-60 seconds | Auto-plays muted |
| Instagram Reels | 9:16 vertical | 15-90 seconds | Vertical only |
| TikTok | 9:16 vertical | 15-60 seconds | Fast pace, hook in first 2 seconds |
| YouTube Shorts | 9:16 vertical | Under 60 seconds | Hook immediately |

---

## Video Types

### Meme Clips (3-10 seconds)
- Iconic TV/movie scene + text overlay
- Works without sound
- Text readable at phone size
- Scene emotion matches the topic

### Text-on-Video (15-30 seconds)
- Stock footage background
- Bold text overlay telling a story
- Each "slide" is 2-4 seconds
- Background music optional

### Demo/Screen Recording (15-60 seconds)
- Show the actual tool/product
- Zoomed in on the relevant part
- Text annotations highlighting key points
- Speed up boring parts

### Talking Head (30-60 seconds)
- Direct to camera
- Strong hook in first 2 seconds
- One point only
- Captions always on

---

## Quality Rules

Every video must pass:

1. **Works without sound?** — Must be understandable on mute (text overlays, visual storytelling)
2. **Hook in 2 seconds?** — First frame grabs attention
3. **Readable at phone size?** — Text large enough for mobile
4. **Under time limit?** — Matches platform specs
5. **One clear message?** — Viewer knows the point within 5 seconds

---

## Video Sources

For stock footage and clips:
- Pexels Videos (free, no attribution)
- Pixabay Videos (free)
- User's own recordings

For meme clips:
- Iconic TV scenes (user provides or describes)
- User's clip library

---

## Text Overlay Rules

- Font: bold, sans-serif, high contrast
- Size: minimum 48px (readable on phone)
- Position: center or upper third (never bottom — UI elements cover it)
- Shadow or background box for readability
- Maximum 8-10 words per frame
- Each text frame visible for 2-4 seconds minimum

---

## Anti-Slop for Video

Video slop shows up in two places: the text overlays and the stock footage.

- **The hook frame is a specific claim, not hype.** "Watch this!", "You won't believe this", "This changes everything" are empty — they'd open any video. Lead with the real detail: "$81K API bill in one week" / "This repo hit 12K stars in 3 days". Apply the generic test to frame 1.
- **Overlay text follows the anti-AI rules.** No puffery ("game-changer"), no triads, no vague quantifiers. Real numbers and names. The specificity layer in `anti-ai-writing.md` applies to every frame.
- **Stock footage: avoid the generic AI-era clichés.** Glowing blue "AI brain" renders, swirling particle networks, faceless hooded hacker, abstract data streams — these are the video equivalent of image slop. Prefer the real thing (screen recording of the actual tool, the real pricing page) or concrete, specific footage over abstract "tech" B-roll.
- **If any frame is an AI-generated image/clip,** its prompt passes the `image-prompts.md` slop check.
- **One real point beats motion graphics.** A plain screen recording that shows the actual thing outperforms a slick animated card that says nothing specific.

---

## Output Format

When creating video content, output:

```markdown
## Video
**Type:** [Meme clip / Text-on-video / Demo / Talking head]
**Duration:** [X seconds]
**Format:** [9:16 / 16:9 / 1:1]
**Script/Storyboard:**
- Frame 1 (0-3s): [description + text overlay]
- Frame 2 (3-6s): [description + text overlay]
- Frame 3 (6-10s): [description + text overlay]
**Audio:** [None / Background music / Voiceover]
**Status:** [Ready / Needs user input]
```
