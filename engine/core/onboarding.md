# Onboarding

When the user first interacts and `my-niche/` is empty or contains only a .gitkeep file, run this onboarding flow.

## First Message

Say exactly:

> "Welcome to post-kit! I'm your content pipeline. I'll help you research, write, and polish posts that sound like you — not AI.
>
> How do you want to set up?
>
> 1. **Guided** — I'll ask you questions and build everything from your answers
> 2. **Manual** — I'll point you to the docs and you configure the files yourself"

Wait for their answer.

---

## If Manual

Respond with:

> "Got it. Here's what you need:
>
> - Read `setup-guide.md` for step-by-step instructions
> - Check `examples/ai-tech/` for a working reference you can study
> - Create your files in `my-niche/` — at minimum you need `niche.yaml` and `voice.md`
>
> Once your files are ready, come back and say 'let's go' and I'll start working with your config."

Stop here. Don't ask more questions.

---

## If Guided

Ask the following questions ONE AT A TIME. Wait for each answer before asking the next. Keep it conversational, not interrogation-style.

### Question 1: Niche
"What do you do? What's your niche or topic area?"

### Question 2: Voice
"How do you want to sound? Pick what's closest, or describe your own:
- Professional and authoritative
- Casual and friendly  
- Savage and opinionated
- Motivational but real
- Educational and clear
- Something else — describe it"

### Question 3: Platforms
"What platforms do you post on? LinkedIn is the default — you can add more:
- LinkedIn only
- LinkedIn + X (Twitter)
- X only
- Other combination — tell me"

### Question 4: Content Pillars
"What do you post about? Give me your main topics and rough percentage split.

For example: 'Workout tips 40%, nutrition myths 30%, client wins 20%, personal life 10%'"

### Question 5: Visuals
"Do you use images or visuals in your posts? (yes/no)"

### Question 5b: Image Tool (only if 5 is yes)
"How do you create your images?
- ChatGPT (GPT Image)
- Gemini / Nano Banana
- Midjourney
- Ideogram / Flux / other — name it
- Canva or manual design (no AI generation)

This tunes how I write image prompts — conversational tools like ChatGPT and Nano Banana want descriptive scenes, while Midjourney-style tools want named styles and tags."

### Question 6: Humor
"Do you do memes, humor, or roasts in your content? (yes/no)"

### Question 7: Content Style
"Is your content mostly:
- News-based (you react to what's happening in your space)
- Evergreen (timeless tips, advice, stories)
- Mix of both"

### Question 8: Audience Hangouts
"Where does your audience hang out online? Which subreddits, communities, forums, or platforms do they use?

If you're not sure, just tell me your niche and I'll suggest some."

### Question 9: Cadence
"How often do you want to post? (e.g., once a day, 3 times a week, twice a day max)"

### Question 10: Timezone
"What timezone are you in? (e.g., EST, GMT, Asia/Karachi)"

### Question 11: Output Folder
"Where do you want posts saved? The default is `posts/YYYY-month/YYYY-MM-DD-slug/`.

If you have an existing content folder or prefer a different structure, tell me. Otherwise just say 'default'."

---

## After All Answers

Generate the following files in `my-niche/`:

### Always generate:
- `niche.yaml` — from answers 1, 3, 4, 9, 10, 11. **Always include `postkit_version`** at the top of the file, set to the current version from the `VERSION` file at the project root. This enables the update system to detect when the user's niche was last synced. Include an `output` field with `path` and `structure` if the user chose a non-default setup (omit the field entirely if they said "default").
- `voice.md` — from answer 2. Include a short "generic test" rule: no caption or line should be reusable under a different topic — it must carry the specific number/name/fact. Specific beats clever.
- `content-rules.md` — from answers 4, 7 (structure, length, hooks based on their style). Include the generic test and a reminder that the strongest anti-slop move is specificity (real numbers/names over vague claims), not a banned-word list.
- `sources.md` — from answer 8
- `hashtags.yaml` — generate relevant hashtags based on their niche and platforms

### Generate if they said yes:
- `visual-system.md` — if answer 5 is yes (customize from `engine/modules/visual-system.md`)
- `image-prompts.md` — if answer 5 is yes AND they generate AI images (customize from `engine/modules/image-prompts.md`). Ask which image tool they use (ChatGPT/GPT Image, Gemini/Nano Banana, Midjourney, etc.) and tune the prompt style to it. Carry over the anti-slop core: brief-not-a-wish, named backgrounds, no vibe adjectives, exact text in quotes, real-media-first.
- `memes.md` — if answer 6 is yes (customize from `engine/modules/memes.md`)

### Generate if news-based or mix:
- `news-scout.md` — if answer 7 includes news (customize from `engine/modules/news-scout.md`)

---

## Confirmation

After generating all files, say:

> "Done! Your content pipeline is ready. Here's what I set up:
>
> [list the files created]
>
> You can start right now. Try:
> - 'Write a post about [topic]'
> - 'What's trending today' (if news-scout is active)
> - 'Help me improve my voice' (brainstorm skill)
>
> Want to change anything? Just tell me or edit the files directly."
