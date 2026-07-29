"""Tests for credits module."""

import pytest
from backend.modules.credits import service


@pytest.fixture(autouse=True)
def use_temp_config(tmp_path, monkeypatch):
    config_path = tmp_path / "config.json"
    monkeypatch.setattr("backend.config.CONFIG_PATH", config_path)
    monkeypatch.setattr("backend.config.DATA_DIR", tmp_path)
    monkeypatch.setattr(
        "backend.modules.credits.service.load_config",
        lambda: _load(config_path),
    )
    monkeypatch.setattr(
        "backend.modules.credits.service.save_config",
        lambda c: _save(config_path, c),
    )


def _load(path):
    import json
    if not path.exists():
        return {
            "plan": {"name": "Free", "limit": 100, "period": "monthly"},
            "usage": {"count": 0, "reset_date": None},
        }
    return json.loads(path.read_text())


def _save(path, config):
    import json
    path.write_text(json.dumps(config))


def test_get_credits():
    credits = service.get_credits()
    assert credits["plan"]["name"] == "Free"
    assert credits["usage"]["count"] == 0


def test_increment_usage():
    new_count = service.increment_usage()
    assert new_count == 1
    new_count = service.increment_usage()
    assert new_count == 2


def test_update_plan():
    result = service.update_plan("Pro", 500, "monthly")
    assert result["name"] == "Pro"
    assert result["limit"] == 500
