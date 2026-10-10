# Quality Gates

Every post must pass ALL of these gates before it's delivered to the user. If it fails any gate, revise and re-check.

---

## Gate 1: Hook Strength

The first 1-2 lines must make someone want to read more.

**Pass if:**
- Opens with a specific claim, number, opinion, or question
- Creates curiosity or tension
- Would make YOU stop scrolling

**Fail if:**
- Opens with generic context-setting ("In the world of...")
- First line could apply to any topic
- No reason to keep reading

---

## Gate 2: One Idea Rule

A post should have one clear idea. Not two. Not three.

**Pass if:**
- You can summarize the post's point in one sentence
- Everything in the post supports that one point
- Nothing feels tangential or "also..."

**Fail if:**
- The post tries to cover multiple topics
- There's a "Also worth mentioning..." section
- Reader would be confused about the main takeaway

---

## Gate 3: Personal Opinion

Every post needs at least one genuine personal take.

**Pass if:**
- Contains a direct opinion ("I think...", "This is dumb", "Nobody's talking about...")
- The opinion is specific enough that someone could disagree
- It reflects the voice in voice.md

**Fail if:**
- Pure information delivery with no stance
- Opinions are hedged into meaninglessness ("It could be argued that...")
- Opinion is so generic nobody could disagree ("Quality matters")

---

## Gate 4: Save or Share Test

The post must pass at least one of these:

- **Save test:** "Would someone bookmark this because they'll want to reference it later?"
  - Has specific numbers, frameworks, comparisons, or actionable advice
- **Share test:** "Would someone send this to a friend or colleague?"
  - Has a strong opinion, surprising take, or entertaining angle

**Fail if:** Neither. It's informative but forgettable. Rewrite with a stronger angle.

---

## Gate 5: Anti-AI Cleanliness

The post must have passed through `engine/core/anti-ai-writing.md`, all five layers, with zero violations remaining.

**Pass if:**
- No Layer 1 words
- No banned structural patterns (negation-affirmation, triads, puffery, drama openers, takeaway closers, hollow framing, hedge-stacking)
- Varied sentence rhythm and openings — reads aloud like a person, not a template
- Transitions are human (not "However/Moreover/Furthermore")
- Has a committed opinion, not balanced mush
- Uses contractions naturally (don't, won't, it's)

**Fail if:** Any banned word or structural pattern remains, OR the "it's not X, it's Y" reframe appears more than once, OR the reasoning is suspiciously clean and non-committal. Run the anti-AI pass again.

**Note on em dashes:** they are NOT an AI tell (Twain and GPT-4.1 use them at nearly identical rates). Do not police them. Use them where they help. Judge the *structure*, not the punctuation.

---

## Gate 5b: Specificity (the highest-leverage structural gate)

The strongest single check for slop. Applies to the caption AND any text baked into the image.

**Pass if:**
- Vague quantifiers ("many", "most", "a lot", "several") are replaced with real numbers wherever possible
- Abstract claims are anchored to concrete things (names, dates, versions, prices, screenshots)
- The post passes **the generic test**: no line could be swapped into a post about a completely different topic unchanged

**Fail if:** The post trades in generalities, or any sentence is so generic it would survive a topic change. Rewrite with the specific stat/name/fact that makes it about THIS story only.

---

## Gate 6: Pillar Alignment

Every post must map to one of the content pillars defined in `my-niche/niche.yaml`.

**Before checking this gate:** Read `my-niche/niche.yaml` and extract the user's `content_pillars` list. Use ONLY those pillar names — never hardcode or assume pillars.

**Pass if:**
- The post clearly belongs to one pillar from the user's niche.yaml
- The post's metadata/front-matter labels it correctly using a pillar that EXISTS in niche.yaml
- The tone matches the pillar's described purpose

**Fail if:**
- Post uses a pillar name that doesn't exist in the user's niche.yaml
- Post doesn't fit any of the user's defined pillars — it's off-topic for the account
- Post tries to span multiple pillars without committing to one angle

**Why this matters:** Platform algorithms reward topic authority. Off-pillar posts dilute your semantic signal. If you want to expand pillars, update niche.yaml FIRST, then post.

---

## Gate 7: Platform Compliance

The post must follow the active platform's rules.

**Check against the relevant platform file:**
- Character count within limits?
- Format appropriate for the platform?
- Links handled correctly (in body vs. in comments)?
- Hashtag count and placement correct?

---

## Gate 7b: Visual Anti-Slop (if the post has a generated image)

For visual-first accounts the image IS the post — a slop image sinks a good caption. If the post uses an AI-generated visual, its prompt must pass the image-prompts slop check.

**Pass if:**
- The prompt contains no vibe adjectives ("beautiful", "sleek", "dramatic", "cinematic", "8K", "professional")
- The specific stat/name/fact is baked into the image, not just the caption
- Background is a named exact color/surface (no default gradient), styling is flat/intentional (no fake glow, no 3D unless deliberate)
- In-image text is quoted, short, placed, with a "no other text" constraint
- The prompt passes **the generic test** — it couldn't describe an image for a different topic

**Fail if:** The prompt is vibe-driven, could produce the generic AI-image look, or a real screenshot exists that would beat it. Fix the prompt or switch to real media. See `image-prompts.md`.

**Skip this gate if:** the post is text-only, or the visual is a real screenshot/sourced media (not generated).

---

## Gate 8: Length Check

Compare against the length rules in `my-niche/content-rules.md`.

- Is it within the specified character/line count for this post type?
- Is it long enough? Compare against the minimum lengths defined in your content-rules.md. Short posts only work when a visual carries the content.
- If the visual carries the content, is the text SHORT?
- No unnecessary padding or filler?

---

## Scoring (Optional)

If the user has analytics.md active, also check:
- Does this topic align with what's historically performed well?
- Is the format/angle similar to past high-performers?

This is informational, not a hard gate. Don't kill a good post because analytics say the topic is untested.

---

## If a Post Fails

1. Identify which gate(s) failed
2. Revise the post targeting those specific failures
3. Re-run from Voice Pass (Step 3 in pipeline) to catch any new issues introduced
4. Re-check all gates

If a post fails the same gate 3 times, flag it to the user:
> "This post is struggling with [gate]. Here's the issue: [explain]. Want me to try a completely different angle, or should I work with what we have?"
