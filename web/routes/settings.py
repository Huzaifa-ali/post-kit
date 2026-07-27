"""Settings route — edit voice, content rules, modules."""

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse

import yaml

from .helpers import templates, MY_NICHE_DIR, PROJECT_ROOT, is_setup_complete

router = APIRouter()

AVAILABLE_MODULES = [
    {"id": "visual-system", "name": "Visual System", "desc": "Recommends image types for each post"},
    {"id": "video-prompts", "name": "Video Prompts", "desc": "Veo3/Runway 30-sec video prompts layered on image prompts"},
    {"id": "memes", "name": "Memes & Humor", "desc": "Humor, roasts, meme formats"},
    {"id": "news-scout", "name": "News Scout", "desc": "Discovers trending topics"},
    {"id": "video-content", "name": "Video Content", "desc": "Short-form video specs and scripts"},
    {"id": "image-prompts", "name": "Image Prompts", "desc": "AI image prompt generation"},
    {"id": "carousel", "name": "Carousel", "desc": "Multi-slide content creation"},
    {"id": "repurpose", "name": "Repurpose", "desc": "Adapts posts for multiple platforms"},
    {"id": "analytics", "name": "Analytics", "desc": "Tracks performance and insights"},
]


@router.get("/settings")
async def settings_page(request: Request):
    if not is_setup_complete():
        return RedirectResponse(url="/onboarding", status_code=302)

    niche_data = {}
    niche_file = MY_NICHE_DIR / "niche.yaml"
    if niche_file.exists():
        with open(niche_file, "r", encoding="utf-8") as f:
            niche_data = yaml.safe_load(f) or {}

    voice_content = ""
    if (MY_NICHE_DIR / "voice.md").exists():
        voice_content = (MY_NICHE_DIR / "voice.md").read_text(encoding="utf-8")

    rules_content = ""
    if (MY_NICHE_DIR / "content-rules.md").exists():
        rules_content = (MY_NICHE_DIR / "content-rules.md").read_text(encoding="utf-8")

    sources_content = ""
    if (MY_NICHE_DIR / "sources.md").exists():
        sources_content = (MY_NICHE_DIR / "sources.md").read_text(encoding="utf-8")

    hashtags_content = ""
    if (MY_NICHE_DIR / "hashtags.yaml").exists():
        hashtags_content = (MY_NICHE_DIR / "hashtags.yaml").read_text(encoding="utf-8")

    active_modules = [mod["id"] for mod in AVAILABLE_MODULES if (MY_NICHE_DIR / f"{mod['id']}.md").exists()]

    return templates.TemplateResponse(request, "settings.html", {
        "niche": niche_data,
        "voice_content": voice_content,
        "rules_content": rules_content,
        "sources_content": sources_content,
        "hashtags_content": hashtags_content,
        "available_modules": AVAILABLE_MODULES,
        "active_modules": active_modules,
        "page": "settings",
    })


@router.post("/settings/voice")
async def save_voice(voice_content: str = Form(...)):
    MY_NICHE_DIR.mkdir(parents=True, exist_ok=True)
    (MY_NICHE_DIR / "voice.md").write_text(voice_content, encoding="utf-8")
    return RedirectResponse(url="/settings?saved=voice", status_code=302)


@router.post("/settings/rules")
async def save_rules(rules_content: str = Form(...)):
    MY_NICHE_DIR.mkdir(parents=True, exist_ok=True)
    (MY_NICHE_DIR / "content-rules.md").write_text(rules_content, encoding="utf-8")
    return RedirectResponse(url="/settings?saved=rules", status_code=302)


@router.post("/settings/sources")
async def save_sources(sources_content: str = Form(...)):
    MY_NICHE_DIR.mkdir(parents=True, exist_ok=True)
    (MY_NICHE_DIR / "sources.md").write_text(sources_content, encoding="utf-8")
    return RedirectResponse(url="/settings?saved=sources", status_code=302)


@router.post("/settings/hashtags")
async def save_hashtags(hashtags_content: str = Form(...)):
    MY_NICHE_DIR.mkdir(parents=True, exist_ok=True)
    (MY_NICHE_DIR / "hashtags.yaml").write_text(hashtags_content, encoding="utf-8")
    return RedirectResponse(url="/settings?saved=hashtags", status_code=302)


@router.post("/settings/modules")
async def save_modules(request: Request):
    form = await request.form()
    selected_modules = form.getlist("modules")
    engine_modules = PROJECT_ROOT / "engine" / "modules"

    for mod in AVAILABLE_MODULES:
        mod_file = MY_NICHE_DIR / f"{mod['id']}.md"
        engine_file = engine_modules / f"{mod['id']}.md"
        if mod["id"] in selected_modules:
            if not mod_file.exists() and engine_file.exists():
                mod_file.write_text(engine_file.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            if mod_file.exists():
                mod_file.unlink()

    niche_file = MY_NICHE_DIR / "niche.yaml"
    if niche_file.exists():
        with open(niche_file, "r", encoding="utf-8") as f:
            niche_data = yaml.safe_load(f) or {}
        niche_data["modules_active"] = list(selected_modules)
        with open(niche_file, "w", encoding="utf-8") as f:
            yaml.dump(niche_data, f, default_flow_style=False, allow_unicode=True)

    return RedirectResponse(url="/settings?saved=modules", status_code=302)
