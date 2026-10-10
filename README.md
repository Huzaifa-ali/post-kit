<div align="center">

# post-kit

<img src="docs/images/post-kit.png" alt="post-kit — Your AI assistant's content engine" width="800"/>

**Your AI assistant's content engine.** Research, write, and publish posts that sound like you — zero code, any niche, any platform.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Works with any AI tool](https://img.shields.io/badge/Works_with-Any_AI_Tool-blue.svg)](#-quick-start)
[![Zero Code](https://img.shields.io/badge/Zero_Code-Markdown_Only-orange.svg)](#-how-it-works)
[![GitHub Template](https://img.shields.io/badge/Use_this-Template-purple.svg)](https://github.com/Huzaifa-ali/post-kit/generate)

[Quick Start](#-quick-start) · [How It Works](#-how-it-works) · [Modules](#-modules) · [Examples](#-examples) · [Contributing](#-contributing)

</div>

---

## What Comes Out

I said _"write a post about why most people quit the gym in January"_ — here's what the pipeline produced:

> 80% of New Year gym memberships are abandoned by February. Not because people are lazy. Because the goal was wrong.
>
> "Get in shape" isn't a goal. It's a vibe. You can't measure a vibe. You can't fail at a vibe clearly enough to course-correct.
>
> Here's what actually sticks:
>
> → "Squat my bodyweight by March" — specific, testable, has a deadline
> → "Go 3x per week for 8 weeks" — system, not outcome
> → "Lose 4kg before my trip in April" — tied to something real
>
> The people still in the gym in March didn't have more discipline. They had a clearer target.
>
> What was the goal that actually got you consistent?

No "delve." No "it's worth noting." No "in today's rapidly evolving landscape." Just a real person with real opinions sharing something useful — in their voice, for their audience.

---

## 🚫 The Anti-AI Pass (Before → After)

<table>
<tr>
<th>❌ Before (raw AI output)</th>
<th>✅ After (anti-AI pass)</th>
</tr>
<tr>
<td>

It's worth noting that in today's rapidly evolving fitness landscape, leveraging a comprehensive gym routine is crucial for fostering long-term wellness. Furthermore, implementing a robust workout strategy empowers individuals to streamline their health journey seamlessly.

</td>
<td>

80% of New Year gym memberships are abandoned by February. Not because people are lazy. Because the goal was wrong. "Get in shape" isn't a goal. It's a vibe. You can't measure a vibe.

</td>
</tr>
</table>

The anti-AI pass runs on **every** post. It's a structural rewrite, not a find-and-replace, working in **five layers** from shallow to deep:

1. **Word choice** — swap the statistical fingerprint words (delve, leverage, robust…). The shallow layer.
2. **Sentence rhythm** — vary length and openings so it doesn't read like a template.
3. **Transitions** — kill "However / Moreover / Furthermore"; use human connectors or none.
4. **Specificity** — _where slop actually dies._ Vague quantifiers → real numbers, abstract nouns → concrete things, every line must pass the generic test.
5. **Thinking patterns** — commit to an opinion, drop false balance, no hedged mush.

It does **not** police em dashes — those aren't an AI tell (Twain and GPT-4.1 use them at nearly the same rate). It judges structure, not punctuation.

---

## ✨ Features

| Feature | What it does |
|---------|-------------|
| 🎙️ **Voice matching** | Learns how you sound — posts read like YOU wrote them |
| 🚫 **Anti-AI filter** | Five-layer structural rewrite on every post — words, rhythm, transitions, specificity, and thinking |
| 🎯 **The generic test** | Flags any line that could survive a topic change and forces a real number, name, or fact in its place |
| 🔍 **Smart research** | Multi-angle web search with source triage, cross-validation, and citation — no MCPs needed |
| 🖼️ **Image-tool aware** | Tunes image prompts to your tool (ChatGPT, Nano Banana, Midjourney…) and slop-checks every prompt |
| 📦 **Modular** | Only enable what you need (visuals, memes, news, video, analytics) |
| 📱 **Multi-platform** | LinkedIn, X, YouTube, Newsletter — one post adapts to many |
| ⚡ **5-minute setup** | Guided onboarding — answer 10 questions, start posting immediately |

---

## 🚀 Quick Start

### 1. Get your own copy

<a href="https://github.com/Huzaifa-ali/post-kit/generate">
  <img src="https://img.shields.io/badge/Use_this_template-green?style=for-the-badge" alt="Use this template"/>
</a>

Click **"Use this template"** on GitHub to create your own copy. Or clone directly:

```bash
git clone https://github.com/Huzaifa-ali/post-kit.git my-content-pipeline
cd my-content-pipeline
```

### 2. Open in your AI tool

Open the folder in **any** AI coding tool:

| Tool | How |
|------|-----|
| **Kiro** | File → Open Folder → select the cloned folder |
| **Claude Code** | `cd my-content-pipeline` then run `claude` |
| **Cursor** | File → Open Folder → select the cloned folder |
| **Windsurf / Cline / Copilot** | Same — open the folder, start chatting |

The AI reads `AGENTS.md` and becomes your content pipeline. Some tools need a one-time wiring step — see [Agent Auto-Discovery](#-agent-auto-discovery) below.

### 3. Set up your pipeline (3 minutes)

Start a conversation. The AI will greet you:

> "Welcome to post-kit! Guided or manual setup?"

Pick **guided**. The AI asks you 10 simple questions:

1. What's your niche? _(fitness, crypto, marketing, cooking — anything)_
2. How do you want to sound? _(casual, professional, savage, educational)_
3. What platforms? _(LinkedIn, X, both, others)_
4. What do you post about? _(your topics + rough percentage split)_
5. Do you use images?
6. Do you do memes/humor?
7. News-based or evergreen content?
8. Where does your audience hang out online?
9. How often do you post?
10. Your timezone?

From your answers, the AI generates your personalized config files in `my-niche/` — your voice profile, content rules, sources, hashtags, and active modules. You own all of it.

### 4. Start posting

Say any of these:

| You say | What happens |
|---------|-------------|
| "Write a post about [topic]" | Full pipeline runs → finished post in `posts/` |
| "What's trending in my space?" | Scouts Reddit, HN, RSS for hot topics |
| "Roast [company/topic]" | Meme pipeline (if humor is enabled) |
| "Help me improve my hooks" | Brainstorms better opening lines with you |
| "Repurpose this for X" | Adapts a LinkedIn post for Twitter format |

Every post goes through: **Dedup Check → Research → Write → Voice Match → Anti-AI Filter → Quality Gate → Output.** If you've already posted about a topic this month, it flags it before wasting time on research.

---

## ⚙️ How It Works

```mermaid
graph LR
    A[Dedup Check] --> B[Research]
    B --> C[Write]
    C --> D[Voice Pass]
    D --> E[Anti-AI Pass]
    E --> F[Quality Gate]
    F --> G[Output]
```

Every post goes through this pipeline automatically:

1. **Dedup Check** — Scans existing posts for the month, flags if you've already covered the topic (runs before any research)
2. **Research** — Multi-angle web search with intent classification, source triage, and cross-validation (powered by `engine/core/web-research.md`)
3. **Write** — Drafts following your content rules (length, structure, hooks)
4. **Voice Pass** — Rewrites to match YOUR voice profile
5. **Anti-AI Pass** — Five-layer structural rewrite: word choice, sentence rhythm, transitions, specificity (the generic test), and thinking patterns _(mandatory, always on)_
6. **Quality Gate** — Checks hook strength, one-idea rule, save/share test, specificity, visual anti-slop, and platform compliance
7. **Output** — Saves to `posts/` with metadata, ready to publish

---

## 📦 Modules

Enable by telling the AI "I want to do [feature]" or by dropping a `.md` file in your config folder.

| Module | What it does |
|--------|-------------|
| **News Scout** | Discovers trending topics, cross-validates across sources |
| **Visual System** | Recommends the right image type for each post |
| **Memes** | Humor, roasts, meme formats with calibration levels |
| **Image Prompts** | Generates AI image prompts when no real image fits |
| **Video Content** | Short-form video specs, scripts, storyboards |
| **Carousel** | Multi-slide content creation |
| **Repurpose** | Adapts one post for multiple platforms |
| **Analytics** | Tracks what works, feeds insights back into the pipeline |

Don't need memes? Don't enable it. Want analytics later? Just ask.

---

## 🔌 Agent Auto-Discovery

Most AI tools don't auto-read `AGENTS.md` unless you wire them up. Here's how to make the pipeline load automatically for each tool — so you just say "write a post" and it works.

| Tool | Config file to create | Location |
|------|----------------------|----------|
| **Kiro** | `.kiro/steering/post-kit.md` | Workspace root (outside `post-kit/`) |
| **Claude Code** | `CLAUDE.md` | Workspace root |
| **Cursor** | `.cursor/rules/post-kit.md` | Inside `post-kit/` or workspace root |
| **Windsurf** | `.windsurfrules` | Workspace root |
| **Copilot** | `.github/copilot-instructions.md` | Workspace root |

### Kiro

Create `.kiro/steering/post-kit.md` at your workspace root:

```markdown
# post-kit Content Pipeline

When the user asks to create, write, draft, brainstorm, or research content,
follow the post-kit pipeline.

## Bootstrap

1. Read `post-kit/AGENTS.md`
2. Read `post-kit/my-niche/niche.yaml` — if missing, run onboarding
3. Follow `post-kit/engine/core/pipeline.md` for every content request
```

Kiro's steering files are always-included by default — the pipeline fires automatically on any content request.

### Claude Code

Create a `CLAUDE.md` at your workspace root:

```markdown
Read and follow `post-kit/AGENTS.md` for all content creation requests.
```

Claude Code reads `CLAUDE.md` automatically at the start of every conversation.

### Cursor

Create `.cursor/rules/post-kit.md` (or `.cursorrules` at workspace root):

```markdown
Read and follow `post-kit/AGENTS.md` for all content creation requests.
Follow the pipeline in `post-kit/engine/core/pipeline.md` for every post.
Always read `post-kit/my-niche/voice.md` and `post-kit/my-niche/content-rules.md` before writing.
```

### Windsurf

Create `.windsurfrules` at your workspace root:

```markdown
Read and follow `post-kit/AGENTS.md` for all content creation requests.
```

### GitHub Copilot

Create `.github/copilot-instructions.md`:

```markdown
Read and follow `post-kit/AGENTS.md` for all content creation requests.
```

### Why is this needed?

AI tools don't scan every markdown file in your project looking for instructions. Each tool has its own specific file it checks at startup. The `AGENTS.md` file is the universal instruction set — the wiring files just tell your specific tool to read it.

If you use multiple AI tools, create the config for each one. They all point to the same `AGENTS.md`, so behavior stays consistent.

---

## 📂 Project Structure

```
post-kit/
├── engine/
│   ├── core/           # Pipeline, onboarding, quality gates, anti-AI pass, web research
│   ├── modules/        # Optional capabilities (news, memes, visuals, etc.)
│   └── platforms/      # Platform-specific rules (LinkedIn, X, etc.)
├── examples/
│   └── ai-tech/        # Complete working niche pack (study or copy)
├── my-niche/           # YOUR config lives here (created during setup)
├── posts/              # Generated posts go here
└── docs/               # Full documentation
```

---

## 🎯 Examples

The [`examples/ai-tech/`](examples/ai-tech/) folder contains a complete, proven niche pack for AI/tech content. It includes voice profile, content rules, sources, hashtags, and active modules — everything configured and working.

Use it to:
- Study how the pieces connect
- Copy it as a starting template for your own niche
- See what good configuration looks like

---

## 🤝 Contributing

We welcome contributions — especially:

- **Niche packs** — Share your working config for others in your niche
- **New modules** — Add capabilities anyone can use
- **Platform files** — Research and document new platforms
- **Anti-AI patterns** — Found a new AI tell? Add it

See [docs/contributing.md](docs/contributing.md) for guidelines.

---

## 🗺️ Roadmap

- [x] Core pipeline (Research → Write → Voice → Anti-AI → Quality Gate → Output)
- [x] Guided onboarding (10-question setup)
- [x] Built-in web research engine (multi-angle search, source triage, no MCPs required)
- [x] LinkedIn platform support
- [x] X (Twitter) platform support
- [x] 8 optional modules (news, memes, visuals, video, carousel, analytics, repurpose, image prompts)
- [x] Five-layer anti-AI pass with the generic test (specificity + visual anti-slop quality gates)
- [x] Image-tool-aware onboarding and prompt tuning (ChatGPT, Nano Banana, Midjourney, etc.)
- [ ] Community niche packs (fitness, crypto, SaaS, real estate, marketing)
- [ ] YouTube Community platform file
- [ ] Newsletter platform file
- [ ] Blog platform file
- [ ] Thread/series module (multi-post storylines)
- [ ] Scheduling integration suggestions (best time to post per platform)
- [ ] A/B hook testing (generate 3 hooks, pick the strongest)
- [ ] Voice calibration from existing posts (paste 5 posts, extract your voice automatically)

Have an idea? [Open a feature request](https://github.com/Huzaifa-ali/post-kit/issues/new?template=feature_request.md).

---

## 📄 License

[MIT](LICENSE) — use it however you want.
