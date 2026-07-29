"""App configuration — loaded from app/data/config.json."""

import json
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = APP_DIR / "data"
CONFIG_PATH = DATA_DIR / "config.json"


def load_config() -> dict:
    """Load config from JSON file. Returns defaults if missing."""
    if not CONFIG_PATH.exists():
        return {"postkit_path": "..", "adapter": "kiro", "theme": "dark"}
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def save_config(config: dict) -> None:
    """Save config to JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(
        json.dumps(config, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def get_postkit_root() -> Path:
    """Resolve the post-kit root directory from config."""
    config = load_config()
    raw_path = config.get("postkit_path", "..")
    resolved = (APP_DIR / raw_path).resolve()
    return resolved
