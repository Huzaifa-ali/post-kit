"""Tests for PostKitBridge."""

import pytest
from pathlib import Path

import yaml

from backend.core.bridge import PostKitBridge


@pytest.fixture
def mock_postkit(tmp_path):
    """Create a minimal post-kit directory structure."""
    niche_dir = tmp_path / "my-niche"
    niche_dir.mkdir()
    posts_dir = tmp_path / "posts"
    posts_dir.mkdir()

    niche_config = {
        "name": "Test Niche",
        "platforms": ["linkedin"],
        "content_pillars": [{"name": "Topic A", "percentage": 60}],
        "modules_active": ["news-scout", "memes"],
        "cadence": {"posts_per_day": 1, "best_days": ["tuesday"]},
        "output": {"path": "posts"},
        "postkit_version": "1.0.0",
    }
    (niche_dir / "niche.yaml").write_text(
        yaml.dump(niche_config), encoding="utf-8"
    )
    (niche_dir / "voice.md").write_text("# Voice\nBe direct.", encoding="utf-8")
    (tmp_path / "VERSION").write_text("1.1.0", encoding="utf-8")

    return tmp_path


def test_is_onboarded(mock_postkit):
    bridge = PostKitBridge(mock_postkit)
    assert bridge.is_onboarded() is True


def test_not_onboarded(tmp_path):
    bridge = PostKitBridge(tmp_path)
    assert bridge.is_onboarded() is False


def test_load_niche_config(mock_postkit):
    bridge = PostKitBridge(mock_postkit)
    config = bridge.load_niche_config()
    assert config["name"] == "Test Niche"
    assert config["platforms"] == ["linkedin"]


def test_get_active_modules(mock_postkit):
    bridge = PostKitBridge(mock_postkit)
    assert bridge.get_active_modules() == ["news-scout", "memes"]


def test_get_posts_path(mock_postkit):
    bridge = PostKitBridge(mock_postkit)
    assert bridge.get_posts_path() == mock_postkit / "posts"


def test_list_niche_files(mock_postkit):
    bridge = PostKitBridge(mock_postkit)
    files = bridge.list_niche_files()
    assert "niche.yaml" in files
    assert "voice.md" in files


def test_read_niche_file(mock_postkit):
    bridge = PostKitBridge(mock_postkit)
    content = bridge.read_niche_file("voice.md")
    assert "Be direct" in content


def test_get_version(mock_postkit):
    bridge = PostKitBridge(mock_postkit)
    assert bridge.get_version() == "1.1.0"
    assert bridge.get_niche_version() == "1.0.0"


def test_write_niche_file(tmp_path):
    bridge = PostKitBridge(tmp_path)
    bridge.write_niche_file("test.md", "# Test content")
    assert (tmp_path / "my-niche" / "test.md").exists()
    assert (tmp_path / "my-niche" / "test.md").read_text(encoding="utf-8") == "# Test content"
