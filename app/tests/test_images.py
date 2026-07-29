"""Tests for the images module."""

import pytest
from backend.modules.images import service


@pytest.fixture(autouse=True)
def use_temp_media(tmp_path, monkeypatch):
    media_dir = tmp_path / "media"
    media_dir.mkdir()
    monkeypatch.setattr(service, "MEDIA_DIR", media_dir)
    monkeypatch.setattr(service, "MANIFEST_PATH", media_dir / "manifest.json")


def test_list_images_empty():
    assert service.list_images() == []


def test_save_and_list_image():
    entry = service.save_uploaded_image("test.png", b"fake-image-data", tags=["hero"])
    assert entry["original_name"] == "test.png"
    assert entry["size_bytes"] == len(b"fake-image-data")
    images = service.list_images()
    assert len(images) == 1


def test_filter_by_tag():
    service.save_uploaded_image("a.png", b"data", tags=["hero"])
    service.save_uploaded_image("b.png", b"data", tags=["meme"])
    assert len(service.list_images(tag="hero")) == 1
    assert len(service.list_images(tag="meme")) == 1


def test_delete_image():
    entry = service.save_uploaded_image("del.png", b"data")
    service.delete_image(entry["filename"])
    assert service.list_images() == []


def test_get_image_path():
    entry = service.save_uploaded_image("path.png", b"content")
    path = service.get_image_path(entry["filename"])
    assert path is not None
    assert path.exists()


def test_get_nonexistent_image_path():
    assert service.get_image_path("nonexistent.png") is None
