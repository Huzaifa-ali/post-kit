# Image Prompts Module

Handles AI image generation when no real screenshot, stock photo, or sourced meme fits the post. Gives the user ready-to-use prompts tuned to how modern image models actually behave.

---

## The Core Principle (why AI images look like slop)

**Vague prompts produce vague images.** A prompt like "a professional, modern graphic, sleek and high-quality" lands in the densest part of the model's training distribution — the output is the average of a million similar images. That average IS the slop look: blue-purple gradients, fake glow, glossy 3D, everything centered, could-be-any-topic blandness.

The fix is not more adjectives. It's **narrowing constraints** — concrete nouns and exact values the model can't average away. A prompt is a **creative brief, not a wish.**

Before any prompt ships, it must pass:

> **The generic test:** Could this exact prompt describe an image for a different topic? If yes, it's too vague. Add the specific number, name, or fact that makes it about THIS post only.

---

## When to Use AI Images

Still a lower priority than real media. Only when:
- No real screenshot exists for the topic
- No stock photo captures it
- The post needs a visual that doesn't exist in reality

NEVER when:
- A real screenshot IS the content
- A sourced meme carries the emotion better
- The post works as text-only
- A weak generated image would be worse than none

See `visual-system.md` for the full media-selection order (real media wins).

---

## Know Your Tool

Modern image tools are **conversational, instruction-following models** (ChatGPT / GPT Image, Google Gemini / Nano Banana, and similar). They want **plain sentences, a stated purpose, and specifics** — not comma-separated keyword soup. If the user's niche uses a keyword-style tool (Midjourney, Flux), adapt: those respond well to named film stocks, lenses, and style tags. For the conversational tools:

- Describe the scene narratively, in sentences.
- **State what the image is FOR** ("a LinkedIn data card for...") — the intended use sets the model's "mode" and polish level.
- Lead with a strong verb for Gemini/Nano Banana ("Create…", "Compose…").
- Use **positive framing** — "empty background", never "no clutter".
- Iterate with small single-change follow-ups rather than one giant prompt.
- Treat generation as a draft: if a word must be exact, the user places it afterward in an editor.

Ask the user which tool they use during setup and tune prompts to it.

---

## The Multi-Prompt System

Every post needing AI images gets **3 prompts** that solve the message in **genuinely different ways** — not the same card in three colors. One should be the straightforward version; at least one should take a different angle entirely (a comparison, a source screenshot framing, a scene). The user picks and generates.

---

## Prompt Anatomy (cover these in sentences — do NOT make it a rigid formula)

1. **Purpose + format** — what it is and what it's for.
2. **Background** — an exact color or surface, never a mood. Name it (#0d1117, deep teal, charcoal). Unspecified backgrounds default to gradient mush.
3. **Hero element** — the one thing the eye lands on first.
4. **Exact text** — in quotes, with the capitalization and placement you want. Font *style* described (heavy condensed sans-serif, thin uppercase), never a named font. Under ~12 visible words.
5. **Layout** — where each element sits.
6. **Style** — chosen deliberately: "flat 2D graphic design", "clean editorial", "photoreal scene".
7. **Hard constraints** — what it must NOT contain ("no glow, no gradient, no 3D, no extra text, no logos").

---

## Text-in-Image Rules

- Exact words in **"quotes"** with intended capitalization.
- Short — the caption is not in the image.
- Placement stated explicitly.
- Font *style* only, never a named font.
- Spell tricky names letter-by-letter.
- Always constrain: "no other text, no random letters, no watermark, no logo."
- For perfect accuracy on a critical word, generate the layout, then place the text in an editor.

---

## Banned From Every Prompt (the vibe words)

These describe the user's *reaction*, not the image. They narrow nothing and pull the output toward the slop average. Delete or replace with a concrete thing:

`beautiful, stunning, sleek, modern, professional, epic, dramatic, cinematic (unless genuinely a photoreal scene), high-quality, hyper-detailed, 8K, masterpiece, award-winning`

Also banned by default (the AI-image look): fake glow, lens flare, floating 3D objects, glossy bevels, and unnamed gradients. For a flat data card there is **no lighting** — it's a flat graphic.

---

## Quality Rules

1. Each of the 3 prompts produces a genuinely different image (different approach, not recolor).
2. One safe/clear option + at least one that reframes the message.
3. Label each prompt with its approach.
4. The specific post detail (number/name/fact) appears in the prompt.
5. First prompt = most likely to land.

---

## Before Handoff — Slop Check

1. **Generic test** — specific detail present? Could it describe another topic?
2. **Vibe-word scan** — any banned adjective? Delete it.
3. **Background named?** — or left to default into gradient mush?
4. **Lighting** — any glow on a flat card? Remove it.
5. **Text** — quoted, short, placed, "no other text" constraint?
6. **Real-media check** — does a real screenshot exist? It wins.

---

## Output Format

```markdown
## Image Prompts
**Type:** AI-generated
**Tool:** [the user's image tool]
**Status:** Prompts ready for user to generate
**Real media available?** [Yes — use screenshot of X / No]

**Prompt 1 — [approach]:**
[plain-sentence brief, specific, no vibe words]
Text in image: "[exact words]"

**Prompt 2 — [a different approach]:**
[reframes the message, not a recolor]
Text in image: "[exact words]"

**Prompt 3 — [another approach]:**
[another direction]
Text in image: "[exact words]"

Pick one and generate. If a word must be exact, place it yourself after generating.
```
