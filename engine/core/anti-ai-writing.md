# Anti-AI Writing

Mandatory pass on EVERY post. Cannot be disabled. Run after the voice pass, before the quality gate.

The goal: make every post read like a specific human with a real opinion wrote it. Not ChatGPT. Not a "thought leader." Not the average of a million LinkedIn posts.

---

## Why a Banned-Word List Is Not Enough

Deleting "delve" and "leverage" is the shallowest possible fix, and on its own it fails. Two reasons:

1. **Slop is structural, not lexical.** You can remove every banned word and still have pure slop, because the *skeleton* is AI: formulaic hooks, negation-then-affirmation, triads, puffery, abstract nouns, and suspiciously clean reasoning. Editors who catch AI do it by reading for these patterns, not by scanning for words.
2. **Surface "tells" are unreliable.** The em dash is the famous example: Mark Twain used ~10 per 1,000 words; GPT-4.1 uses about the same. Em dashes are not an AI signal. Policing them wastes effort on a non-problem. Write naturally; use them when they help.

So this pass works in **five layers, from shallow to deep.** The deep layers matter most.

---

## Layer 1 — Word Choice (shallow, do it fast)

A short list of words that appear disproportionately in AI output. They're not evil; they're statistical fingerprints. Replace with plainer language:

delve, leverage, utilize, facilitate, streamline, foster, empower, harness, robust, comprehensive, seamless, holistic, scalable, innovative, groundbreaking, revolutionize, game-changer, cutting-edge, unlock, boast, navigate (figurative), landscape (figurative), ecosystem (figurative), tapestry, realm, paradigm, synergy.

Rule: if you can't say what is "robust" or "comprehensive", the word is filler — cut it or name the specific thing.

This layer removes the obvious fingerprints. It does not make writing human. Keep going.

---

## Layer 2 — Sentence Rhythm

AI writes in a narrow rhythm band: short punchy sentence, medium explanatory sentence, repeat. Correct-sounding and dead.

- **Vary length hard.** Mix 4-word fragments with the occasional long, winding sentence. Human writing has outliers; AI clusters in the middle.
- **Vary sentence openings.** AI loves subject-verb-object every time ("The model does X. The company said Y."). Start some sentences with a clause, an adverb, or a fragment.
- **Use purposeful fragments.** "Then they deleted it." "Same task. Ten times the price." Fragments create emphasis and are rare in AI training data.
- **Read it aloud.** If every sentence fits one comfortable breath, it's too regular. Where you'd naturally stumble or rush is where a human wrote it.

---

## Layer 3 — Transitions

AI transitions are tidy and identical: "However," "Moreover," "Furthermore," "Additionally," "In conclusion." Dead giveaways.

- Cut them. Replace with "But", "So", "And", a paragraph break, or nothing.
- **Echo transitions** instead: repeat a word from the previous line to carry momentum. "The detector flagged it. That flag cost him the job." No connective word, clear link.
- Sometimes don't transition at all. Jump to the next thought. Humans do.

---

## Layer 4 — Specificity (this is where slop dies)

The single strongest anti-slop move. AI defaults to abstraction because it has read everything and experienced nothing.

- **Replace vague quantifiers with real numbers.** Not "many companies" — "the three labs that shipped this week." Not "prices went up a lot" — "$20 to $0.03 per call, overnight."
- **Replace abstract nouns with concrete things** you could point at, screenshot, or photograph. If removing an abstraction kills the sentence, the sentence was empty — delete it.
- **Name names, dates, versions.** "A February benchmark" beats "recent research."
- **The generic test:** read each line and ask — *could this exact sentence appear in a post about a completely different topic?* If it works for your topic AND for "how to cook pasta," it's generic. Cut it or make it specific to THIS story.

---

## Layer 5 — Thinking Patterns (the deepest tell)

AI reasoning is too clean. It builds a tidy argument, acknowledges the counterpoint at the polite moment, lands a balanced conclusion. Humans don't think like that.

- **Commit to a take.** Don't say "it depends" or "there are pros and cons." Pick a side. A post that makes 20% of readers disagree beats one that bores everyone.
- **Drop false balance.** "While X has merits, Y is better" — if Y is better, just say Y is better.
- **State opinions without hedging them into mush.** "It could be argued that…" is a non-opinion. "This pricing is a bait-and-switch" is an opinion.
- Let the reasoning be a little human: a direct claim, then the evidence, without the textbook scaffolding.

---

## Banned Patterns (structural — these survive a word-swap)

Catch and rewrite these even when no banned word is present:

- **Negation-then-affirmation:** "It's not X, it's Y." / "It wasn't about the money — it was about the principle." A rhythm crutch. State Y alone. Fine *once* per post as a signature move; banned as a per-paragraph habit.
- **Triads:** three-item lists where the third is longest ("fast, reliable, and built to scale with your team"). Pick the one true item.
- **Puffery:** "stands as a testament to", "plays a vital role", "a game-changer for the industry", "marks a watershed moment." Delete; state the fact.
- **The drama opener:** "In today's fast-paced world…", "In an era where…", "As we navigate…". Delete; the reader knows what year it is.
- **The takeaway closer:** a final sentence that restates the opening as a lesson ("And that's why X matters."). End on the last real point.
- **Hollow framing:** "It's important to note that", "It's worth mentioning that". Delete the frame, keep the fact.
- **Hedge-stacking:** "it may be possible that, in some cases, you might consider." One hedge or none.
- **Engagement bait:** "Let that sink in", "Read that again", "Unpopular opinion:" (when it's popular), "Hot take:" (when it's room temperature).
- **Weak linking verbs:** "serves as", "stands as", "represents", "aims to" → use "is" or state the action.

---

## Visual Slop (this account is often visual-first — don't skip)

The same disease infects images. A vague image prompt averages into the same mush every AI image looks like. When a post has a generated visual, the anti-slop pass covers the prompt too:

- No vibe adjectives in prompts ("beautiful", "sleek", "dramatic", "cinematic", "8K"). They narrow nothing.
- The specific stat/name/fact must be baked into the image.
- Exact text in quotes, short, placed, with a "no other text" constraint.
- Named background and flat styling — no default gradient, no fake glow, no 3D.
- Real screenshot beats a generated card whenever the real thing exists.

Full detail lives in the image-prompts module. The point here: a slop image sinks a good caption. Check both.

---

## The Check (run in order)

1. **Specificity pass (do this FIRST):** every vague quantifier → real number? Every abstract claim → concrete thing? Does it pass the generic test?
2. **Thinking pass:** is there a committed opinion, or is it balanced mush?
3. **Pattern pass:** any banned structural pattern? Rewrite it.
4. **Rhythm pass:** read aloud. Varied length and openings? Any purposeful fragments?
5. **Transition pass:** any "However/Moreover/Furthermore"? Replace or cut.
6. **Word pass (last, it's the shallowest):** any Layer 1 word? Swap it.
7. **Visual pass:** if there's a generated image, run its slop check.

If fixing one thing introduces another pattern, fix that too. Repeat until clean.

> Order matters. Most people start with the word list and stop there — that's why their output still reads as AI. Start with specificity and opinion. The words are the easy part.
