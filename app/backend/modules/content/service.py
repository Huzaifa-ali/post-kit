"""Content service — manages adapter sessions and message flow."""

from collections.abc import AsyncGenerator

from backend.adapters.base import BaseAdapter


class ContentService:
    """Manages content creation sessions with the AI adapter."""

    def __init__(self, adapter: BaseAdapter):
        self._adapter = adapter

    async def start_session(self) -> str:
        """Start a new adapter session."""
        return await self._adapter.start_session()

    async def send_message(
        self, message: str, session_id: str | None = None
    ) -> AsyncGenerator[str, None]:
        """Send a message and yield streaming response."""
        async for chunk in self._adapter.send_message(message, session_id):
            yield chunk

    async def end_session(self, session_id: str) -> None:
        """End an adapter session."""
        await self._adapter.end_session(session_id)

    async def is_adapter_available(self) -> bool:
        """Check if the adapter is ready."""
        return await self._adapter.is_available()

    def get_adapter_name(self) -> str:
        """Get the adapter display name."""
        return self._adapter.get_name()
