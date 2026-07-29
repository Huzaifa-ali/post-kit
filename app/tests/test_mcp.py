"""Tests for MCP client and registry."""

import pytest
from unittest.mock import patch

from backend.mcp.registry import get_configured_servers, has_image_server
from backend.mcp.client import MCPClient


def test_no_servers_configured(monkeypatch):
    monkeypatch.setattr(
        "backend.mcp.registry.load_config",
        lambda: {"adapter": "kiro"},
    )
    assert get_configured_servers() == {}
    assert has_image_server() is False


def test_has_image_server(monkeypatch):
    monkeypatch.setattr(
        "backend.mcp.registry.load_config",
        lambda: {"mcp_servers": {"img": {"command": "uvx", "args": [], "disabled": False}}},
    )
    assert has_image_server() is True


def test_disabled_server_not_returned(monkeypatch):
    monkeypatch.setattr(
        "backend.mcp.registry.load_config",
        lambda: {"mcp_servers": {"img": {"command": "uvx", "args": [], "disabled": True}}},
    )
    assert has_image_server() is False


@pytest.mark.asyncio
@patch("backend.mcp.client.asyncio.create_subprocess_exec", side_effect=FileNotFoundError)
async def test_mcp_client_connect_fails(mock_exec):
    client = MCPClient("nonexistent", [])
    result = await client.connect()
    assert result is False


@pytest.mark.asyncio
async def test_mcp_client_call_without_connect():
    client = MCPClient("cmd", [])
    result = await client.call_tool("test", {})
    assert "error" in result


@pytest.mark.asyncio
async def test_mcp_client_is_connected_false_initially():
    client = MCPClient("cmd", [])
    assert client.is_connected is False
