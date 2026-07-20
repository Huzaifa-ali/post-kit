# Changelog

All notable changes to post-kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [1.0.1] - 2026-07-20

### Added
- **Dedup Check (Step 0)** — pipeline now scans existing posts for the current month before running any research or web search. Flags duplicate/overlapping topics and asks the user to confirm, find a fresh angle, or pick a different topic. Saves time and tokens.

### Changed
- Pipeline flow updated: `Request → Dedup Check → Research → Write → Voice Pass → Anti-AI Pass → Quality Gate → Output`
- README hero diagram and step list updated to reflect the new pipeline order
- Image Prompts module updated to 3-prompt system (Text Card / Meme / Scene + Text Overlay)

---

## [1.0.0] - 2026-07-12

### Added
- Complete content pipeline: Research → Write → Voice Pass → Anti-AI Pass → Quality Gate → Output
- Guided onboarding flow (10 questions, 3-minute setup)
- Manual setup path with templates and reference examples
- Anti-AI writing pass with 50+ banned words and pattern detection
- Quality gates: hook strength, one-idea rule, personal opinion, save/share test, platform compliance, length check
- Voice matching system with configurable voice profiles
- Modular architecture — enable/disable features by adding/removing files

### Modules
- News Scout — trending topic discovery with cross-validation
- Visual System — image type recommendations per post
- Memes — humor/roast pipeline with calibration levels
- Image Prompts — AI image generation prompts (4-prompt system)
- Video Content — short-form video specs, scripts, storyboards
- Carousel — multi-slide content creation
- Repurpose — multi-platform content adaptation
- Analytics — performance tracking and feedback loop

### Platforms
- LinkedIn (default)
- X (Twitter)

### Examples
- Complete AI/tech niche pack (`examples/ai-tech/`)

### Compatibility
- Kiro (Powers)
- Claude Code (Plugin)
- Cursor (Rules/Skills)
- Any AI tool that reads markdown files
