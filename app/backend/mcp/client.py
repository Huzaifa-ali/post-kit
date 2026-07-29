"""MCP client — spawns and communicates with MCP servers via stdio JSON-RPC."""

import asyncio
import json
import logging

logger = logging.getLogger(__name__)


class MCPClient:
    """Client that spawns an MCP server process and communicates via stdio."""

    def __init__(self, command: str, args: list[str], env: dict | None = None):
        self._command = command
        self._args = args
        self._env = env
        self._process: asyncio.subprocess.Process | None = None

    async def connect(self) -> bool:
        """Spawn the MCP server process."""
        try:
            self._process = await asyncio.create_subprocess_exec(
                self._command, *self._args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            logger.info(f"MCP server started: {self._command}")
            return True
        except FileNotFoundError:
            logger.error(f"MCP server not found: {self._command}")
            return False

    async def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """Call a tool on the MCP server via JSON-RPC."""
        if not self._process or not self._process.stdin or not self._process.stdout:
            return {"error": "MCP server not connected"}

        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
            "id": 1,
        }

        self._process.stdin.write(json.dumps(request).encode() + b"\n")
        await self._process.stdin.drain()

        try:
            line = await asyncio.wait_for(
                self._process.stdout.readline(), timeout=60.0
            )
            if line:
                return json.loads(line.decode())
            return {"error": "No response from MCP server"}
        except asyncio.TimeoutError:
            return {"error": "MCP server timed out"}

    async def disconnect(self) -> None:
        """Terminate the MCP server process."""
        if self._process and self._process.returncode is None:
            self._process.terminate()
            try:
                await asyncio.wait_for(self._process.wait(), timeout=3.0)
            except asyncio.TimeoutError:
                self._process.kill()
            logger.info("MCP server disconnected")

    @property
    def is_connected(self) -> bool:
        """Check if the server process is still running."""
        return self._process is not None and self._process.returncode is None
