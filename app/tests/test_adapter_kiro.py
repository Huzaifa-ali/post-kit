"""Tests for the Kiro CLI adapter."""

import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock

from backend.adapters.kiro import KiroAdapter


@pytest.fixture
def adapter(tmp_path) -> KiroAdapter:
    return KiroAdapter(tmp_path)


def test_adapter_name(adapter):
    assert adapter.get_name() == "Kiro CLI"


@pytest.mark.asyncio
@patch("backend.adapters.kiro.asyncio.create_subprocess_exec")
async def test_is_available_when_installed(mock_exec, adapter):
    mock_proc = AsyncMock()
    mock_proc.returncode = 0
    mock_proc.wait = AsyncMock(return_value=0)
    mock_exec.return_value = mock_proc
    assert await adapter.is_available() is True


@pytest.mark.asyncio
@patch("backend.adapters.kiro.asyncio.create_subprocess_exec", side_effect=FileNotFoundError)
async def test_is_available_when_not_installed(mock_exec, adapter):
    assert await adapter.is_available() is False


@pytest.mark.asyncio
@patch("backend.adapters.kiro.asyncio.create_subprocess_exec")
async def test_start_session_returns_id(mock_exec, adapter):
    mock_proc = AsyncMock()
    mock_proc.stdin = MagicMock()
    mock_proc.stdout = AsyncMock()
    mock_proc.stderr = AsyncMock()
    mock_proc.returncode = None
    mock_exec.return_value = mock_proc

    session_id = await adapter.start_session()
    assert session_id is not None
    assert len(session_id) == 36  # UUID format


@pytest.mark.asyncio
@patch("backend.adapters.kiro.asyncio.create_subprocess_exec")
async def test_end_session_terminates_process(mock_exec, adapter):
    mock_proc = AsyncMock()
    mock_proc.stdin = MagicMock()
    mock_proc.stdout = AsyncMock()
    mock_proc.stderr = AsyncMock()
    mock_proc.returncode = None
    mock_proc.terminate = MagicMock()
    mock_proc.wait = AsyncMock(return_value=0)
    mock_exec.return_value = mock_proc

    session_id = await adapter.start_session()
    await adapter.end_session(session_id)
    mock_proc.terminate.assert_called_once()


@pytest.mark.asyncio
async def test_end_nonexistent_session_does_nothing(adapter):
    await adapter.end_session("nonexistent-id")  # Should not raise
