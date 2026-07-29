"""Tests for the brand module."""

import pytest

from backend.core.bridge import PostKitBridge
from backend.modules.brand import service


@pytest.fixture
def bridge_with_files(tmp_path) -> PostKitBridge:
    niche_dir = tmp_path / "my-niche"
    niche_dir.mkdir()
    (niche_dir / "voice.md").write_text(
        "# Voice\nBe direct and opinionated.", encoding="utf-8"
    )
    (niche_dir / "niche.yaml").write_text(
        "name: Test\nplatforms: [linkedin]", encoding="utf-8"
    )
    return PostKitBridge(tmp_path)


def test_list_niche_files(bridge_with_files):
    files = service.list_niche_files(bridge_with_files)
    filenames = [f["filename"] for f in files]
    assert "voice.md" in filenames
    assert "niche.yaml" in filenames


def test_file_summary_extracted(bridge_with_files):
    files = service.list_niche_files(bridge_with_files)
    voice_file = next(f for f in files if f["filename"] == "voice.md")
    assert "Voice" in voice_file["summary"]


def test_get_file_content(bridge_with_files):
    content = service.get_file_content(bridge_with_files, "voice.md")
    assert "Be direct" in content


def test_get_nonexistent_file(bridge_with_files):
    content = service.get_file_content(bridge_with_files, "missing.md")
    assert content is None


def test_save_file_content(bridge_with_files):
    service.save_file_content(bridge_with_files, "voice.md", "# Updated\nNew content.")
    content = service.get_file_content(bridge_with_files, "voice.md")
    assert "New content" in content


def test_list_empty_niche(tmp_path):
    bridge = PostKitBridge(tmp_path)
    files = service.list_niche_files(bridge)
    assert files == []
