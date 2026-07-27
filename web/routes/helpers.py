"""Shared utilities for web routes."""

from pathlib import Path

from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent
TEMPLATES_DIR = BASE_DIR / "templates"
MY_NICHE_DIR = PROJECT_ROOT / "my-niche"
POSTS_DIR = PROJECT_ROOT / "posts"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def is_setup_complete() -> bool:
    """Check if onboarding has been completed."""
    return (MY_NICHE_DIR / "niche.yaml").exists()
