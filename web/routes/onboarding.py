"""Onboarding route — guided setup wizard with content goal, tagging, video, engagement."""

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse

import yaml

from .helpers import templates, MY_NICHE_DIR, is_setup_complete

router = APIRouter()


@router.get("/onboarding")
async def onboarding_page(request: Request):
    if is_setup_complete():
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse(request, "onboarding.html", {"page": "onboarding"})


@router.post("/onboarding")
async def onboarding_submit(
    request: Request,
    niche: str = Form(...),
    content_goal: str = Form("meme_viral"),
    voice: str = Form("Savage and meme-literate"),
    voice_custom: str = Form(""),
    platforms: str = Form("linkedin,twitter,instagram,reddit"),
    pillars: str = Form(""),
    visuals: str = Form("yes"),
    video_prompts: str = Form("yes"),
    humor: str = Form("yes"),
    tagging: str = Form("ask"),
    engagement_style: str = Form("debate"),
    content_style: str = Form("mix"),
    audience_hangouts: str = Form(""),
    cadence: str = Form("1-2x daily"),
    timezone: str = Form("Asia/Karachi"),
):
    """Process onboarding and generate all config files."""
    MY_NICHE_DIR.mkdir(parents=True, exist_ok=True)

    # Parse pillars
    pillar_list = []
    for line in pillars.strip().split("\n"):
        line = line.strip().strip("-").strip()
        if line:
            parts = line.rsplit(" ", 1)
            if len(parts) == 2 and parts[1].replace("%", "").isdigit():
                pillar_list.append({"name": parts[0].strip(), "percentage": int(parts[1].replace("%", ""))})
            else:
                pillar_list.append({"name": line, "percentage": 0})
    if not pillar_list:
        # Defaults based on content goal
        if content_goal == "meme_viral":
            pillar_list = [{"name": "Meme reactions", "percentage": 35}, {"name": "Comparisons/roasts", "percentage": 25},
                          {"name": "Educational memes", "percentage": 20}, {"name": "Hot takes", "percentage": 10}, {"name": "Build in public", "percentage": 10}]
        elif content_goal == "educational":
            pillar_list = [{"name": "Tutorials/how-tos", "percentage": 40}, {"name": "News + insight", "percentage": 30},
                          {"name": "Personal lessons", "percentage": 20}, {"name": "Opinion", "percentage": 10}]
        elif content_goal == "storytelling":
            pillar_list = [{"name": "Personal stories", "percentage": 35}, {"name": "Build in public", "percentage": 30},
                          {"name": "Lessons learned", "percentage": 20}, {"name": "News reaction", "percentage": 15}]
        else:
            pillar_list = [{"name": "Industry insight", "percentage": 40}, {"name": "News analysis", "percentage": 30},
                          {"name": "Opinion/takes", "percentage": 20}, {"name": "Case studies", "percentage": 10}]

    total_pct = sum(p["percentage"] for p in pillar_list)
    if total_pct == 0 and pillar_list:
        for p in pillar_list:
            p["percentage"] = 100 // len(pillar_list)

    platform_list = [p.strip() for p in platforms.split(",") if p.strip()]
    voice_label = voice_custom if voice == "custom" else voice

    # --- Write niche.yaml ---
    modules = []
    if visuals.lower() == "yes":
        modules.append("visual-system")
    if humor.lower() == "yes":
        modules.append("memes")
    if content_style.lower() in ("news-based", "mix"):
        modules.append("news-scout")
    if video_prompts.lower() == "yes":
        modules.append("video-prompts")

    niche_data = {
        "name": niche,
        "identity": {"description": f"{niche} content creator", "personality": voice_label},
        "platforms": platform_list,
        "content_pillars": pillar_list,
        "content_goal": content_goal,
        "cadence": {"frequency": cadence, "timezone": timezone},
        "preferences": {"tagging": tagging, "engagement_style": engagement_style},
        "modules_active": modules,
    }
    with open(MY_NICHE_DIR / "niche.yaml", "w", encoding="utf-8") as f:
        yaml.dump(niche_data, f, default_flow_style=False, allow_unicode=True)

    # --- Write voice.md ---
    voice_content = f"""# Voice Profile

## Sound Like
{voice_label}

## Rules
- First-person, conversational
- State opinions directly — no hedging
- Short punchy sentences
- No corporate speak
- Be authentic and real
- Numbers > adjectives
- Specificity > vagueness

## Engagement Style
Default CTA: {engagement_style}

## Tagging
Default: {tagging}

## Never Sound Like
- Corporate press release
- AI trying to sound human
- Generic motivational speaker
- Engagement bait without substance
- Meme page with zero insight
"""
    (MY_NICHE_DIR / "voice.md").write_text(voice_content, encoding="utf-8")

    # --- Write content-rules.md ---
    content_rules = f"""# Content Rules

## Content Goal: {content_goal}

## Structure
```
[Hook — immediately grabs attention]
[Body — substance, insight, humor]
[CTA — {engagement_style}]
```

## Platforms: {', '.join(platform_list)}

## Tagging: {tagging}
## Engagement: {engagement_style}
## Video Prompts: {video_prompts}

## Pillars
"""
    for p in pillar_list:
        content_rules += f"- {p['name']} ({p['percentage']}%)\n"

    content_rules += f"""
## Mandatory Rules
- ONE idea per post
- Hook in first line
- Sources & research — always back claims
- Engagement hook at the end
- Platform-specific formatting (no hashtags on X/Reddit, etc.)
- Quality over speed, but speed matters for news
"""
    (MY_NICHE_DIR / "content-rules.md").write_text(content_rules, encoding="utf-8")

    # --- Write sources.md ---
    (MY_NICHE_DIR / "sources.md").write_text(f"""# Sources

## Audience Hangouts
{audience_hangouts if audience_hangouts else "TBD — update in settings"}

## Source Tiers
- Tier 1 (official): share freely
- Tier 2 (press): attribute
- Tier 3 (blogs): add context
- Tier 4 (social): verify first
""", encoding="utf-8")

    # --- Copy module files from engine ---
    engine_modules = MY_NICHE_DIR.parent / "engine" / "modules"
    for mod in modules:
        engine_file = engine_modules / f"{mod}.md"
        niche_file = MY_NICHE_DIR / f"{mod}.md"
        if engine_file.exists() and not niche_file.exists():
            niche_file.write_text(engine_file.read_text(encoding="utf-8"), encoding="utf-8")

    # Video prompts module (custom, not in engine)
    if video_prompts.lower() == "yes" and not (MY_NICHE_DIR / "video-prompts.md").exists():
        (MY_NICHE_DIR / "video-prompts.md").write_text("""# Video Prompts Module
Generate 30-sec video prompts (Veo3/Runway) layered on image prompts.
Pipeline: Image Prompt (base frame) -> Video Prompt (motion + voiceover)
""", encoding="utf-8")

    return RedirectResponse(url="/dashboard", status_code=302)
