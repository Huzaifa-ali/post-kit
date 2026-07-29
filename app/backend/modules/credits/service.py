"""Credits service — plan display and usage tracking."""

from datetime import date

from backend.config import load_config, save_config


def get_credits() -> dict:
    """Get current plan and usage."""
    config = load_config()
    plan = config.get("plan", {"name": "Free", "limit": 100, "period": "monthly"})
    usage = config.get("usage", {"count": 0, "reset_date": None})
    _check_reset(config, usage)
    return {"plan": plan, "usage": usage}


def increment_usage() -> int:
    """Increment usage counter. Returns new count."""
    config = load_config()
    usage = config.get("usage", {"count": 0, "reset_date": None})
    usage["count"] = usage.get("count", 0) + 1
    config["usage"] = usage
    save_config(config)
    return usage["count"]


def update_plan(name: str, limit: int, period: str) -> dict:
    """Update plan info."""
    config = load_config()
    config["plan"] = {"name": name, "limit": limit, "period": period}
    save_config(config)
    return config["plan"]


def _check_reset(config: dict, usage: dict) -> None:
    """Reset usage if period has elapsed."""
    reset_date_str = usage.get("reset_date")
    if not reset_date_str:
        today = date.today()
        if today.month == 12:
            next_reset = date(today.year + 1, 1, 1)
        else:
            next_reset = date(today.year, today.month + 1, 1)
        usage["reset_date"] = next_reset.isoformat()
        config["usage"] = usage
        save_config(config)
        return

    reset_date = date.fromisoformat(reset_date_str)
    if date.today() >= reset_date:
        usage["count"] = 0
        if reset_date.month == 12:
            next_reset = date(reset_date.year + 1, 1, 1)
        else:
            next_reset = date(reset_date.year, reset_date.month + 1, 1)
        usage["reset_date"] = next_reset.isoformat()
        config["usage"] = usage
        save_config(config)
