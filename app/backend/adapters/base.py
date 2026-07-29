"""Base adapter interface — all AI tool adapters implement this."""

from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from pathlib import Path


class BaseAdapter(ABC):
    """Abstract interface for AI CLI tool adapters."""

    def __init__(self, postkit_root: Path):
        self._postkit_root = postkit_root

    @abstractmethod
    async def send_message(
        self, message: str, session_id: str | None = None
    ) -> AsyncGenerator[str, None]:
        """Send a message, yield streaming response chunks."""
        ...

    @abstractmethod
    async def start_session(self) -> str:
        """Start a persistent CLI session. Returns session_id."""
        ...

    @abstractmethod
    async def end_session(self, session_id: str) -> None:
        """Close a persistent session and kill the process."""
        ...

    @abstractmethod
    async def is_available(self) -> bool:
        """Check if the CLI tool is installed and reachable."""
        ...

    @abstractmethod
    def get_name(self) -> str:
        """Return display name of the adapter."""
        ...
