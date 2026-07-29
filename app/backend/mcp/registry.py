"""MCP server registry — discovers available servers from config."""

from backend.config import load_config


def get_configured_servers() -> dict[str, dict]:
    """Get all configured MCP servers from app config."""
    config = load_config()
    return config.get("mcp_servers", {})


def get_image_server() -> dict | None:
    """Get the configured image generation MCP server, if any."""
    servers = get_configured_servers()
    for name, server_config in servers.items():
        if server_config.get("disabled", False):
            continue
        return {"name": name, **server_config}
    return None


def has_image_server() -> bool:
    """Check if any image MCP server is configured and enabled."""
    return get_image_server() is not None
