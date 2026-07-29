"""Kiro CLI adapter — spawns kiro-cli chat as a subprocess."""

import asyncio
import uuid
import logging
from collections.abc import AsyncGenerator
from pathlib import Path

from backend.adapters.base import BaseAdapter

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 120.0


class KiroAdapter(BaseAdapter):
    """Adapter for Kiro CLI (kiro-cli chat command)."""

    def __init__(self, postkit_root: Path):
        super().__init__(postkit_root)
        self._sessions: dict[str, asyncio.subprocess.Process] = {}

    def get_name(self) -> str:
        return "Kiro CLI"

    async def is_available(self) -> bool:
        """Check if kiro-cli is installed."""
        try:
            proc = await asyncio.create_subprocess_exec(
                "kiro-cli", "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await proc.wait()
            return proc.returncode == 0
        except FileNotFoundError:
            return False

    async def start_session(self) -> str:
        """Spawn a kiro-cli chat process."""
        session_id = str(uuid.uuid4())
        proc = await asyncio.create_subprocess_exec(
            "kiro-cli", "chat",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(self._postkit_root),
        )
        self._sessions[session_id] = proc
        logger.info(f"Started Kiro session: {session_id}")
        return session_id

    async def send_message(
        self, message: str, session_id: str | None = None
    ) -> AsyncGenerator[str, None]:
        """Send message to Kiro CLI and stream response chunks."""
        if session_id and session_id in self._sessions:
            proc = self._sessions[session_id]
        else:
            session_id = await self.start_session()
            proc = self._sessions[session_id]

        if proc.stdin is None or proc.stdout is None:
            yield "[Error: Process streams not available]"
            return

        proc.stdin.write(f"{message}\n".encode())
        await proc.stdin.drain()

        try:
            while True:
                line = await asyncio.wait_for(
                    proc.stdout.readline(), timeout=DEFAULT_TIMEOUT
                )
                if not line:
                    break
                decoded = line.decode("utf-8", errors="replace")
                yield decoded
        except asyncio.TimeoutError:
            yield "[Response timed out]"

    async def end_session(self, session_id: str) -> None:
        """Kill the Kiro CLI process for this session."""
        proc = self._sessions.pop(session_id, None)
        if proc is None:
            return
        if proc.returncode is None:
            proc.terminate()
            try:
                await asyncio.wait_for(proc.wait(), timeout=3.0)
            except asyncio.TimeoutError:
                proc.kill()
        logger.info(f"Ended Kiro session: {session_id}")
