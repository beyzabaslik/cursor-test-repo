"""Cursor MCP provider using stdio JSON-RPC transport."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from app.providers.base import MCPProvider, ProviderStatus

logger = logging.getLogger(__name__)


class CursorStdioMCPProvider(MCPProvider):
    """Spawn a local MCP server process and communicate over stdio."""

    name = "cursor-mcp"

    def __init__(self, command: str, args: list[str], cwd: str | None = None) -> None:
        self._command = command
        self._args = args
        self._cwd = cwd
        self._process: asyncio.subprocess.Process | None = None
        self._request_id = 0
        self._lock = asyncio.Lock()

    async def connect(self) -> None:
        if self._process and self._process.returncode is None:
            return

        self._process = await asyncio.create_subprocess_exec(
            self._command,
            *self._args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self._cwd,
        )
        await self._initialize_session()

    async def disconnect(self) -> None:
        if not self._process:
            return
        if self._process.returncode is None:
            self._process.terminate()
            try:
                await asyncio.wait_for(self._process.wait(), timeout=5)
            except asyncio.TimeoutError:
                self._process.kill()
                await self._process.wait()
        self._process = None

    async def list_tools(self) -> list[dict[str, Any]]:
        await self.connect()
        response = await self._request("tools/list", {})
        return response.get("tools", [])

    async def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        await self.connect()
        response = await self._request(
            "tools/call",
            {"name": name, "arguments": arguments or {}},
        )
        return {
            "content": response.get("content", []),
            "isError": response.get("isError", False),
        }

    async def health_check(self) -> ProviderStatus:
        try:
            await self.connect()
            tools = await self.list_tools()
            return ProviderStatus(
                connected=True,
                provider=self.name,
                message="Cursor MCP stdio provider connected",
                tools=[tool.get("name", "") for tool in tools if tool.get("name")],
            )
        except Exception as exc:  # pragma: no cover - surfaced via status payload
            logger.warning("Cursor MCP health check failed: %s", exc)
            return ProviderStatus(
                connected=False,
                provider=self.name,
                message=str(exc),
                tools=[],
            )

    async def _initialize_session(self) -> None:
        init_response = await self._request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "company-brain-bridge", "version": "1.0.0"},
            },
        )
        if "serverInfo" not in init_response:
            raise RuntimeError("MCP initialize failed")
        await self._notify("notifications/initialized", {})

    async def _notify(self, method: str, params: dict[str, Any]) -> None:
        if not self._process or not self._process.stdin:
            raise RuntimeError("MCP process is not running")
        payload = {"jsonrpc": "2.0", "method": method, "params": params}
        self._process.stdin.write((json.dumps(payload) + "\n").encode())
        await self._process.stdin.drain()

    async def _request(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        async with self._lock:
            if not self._process or not self._process.stdin or not self._process.stdout:
                raise RuntimeError("MCP process is not running")

            self._request_id += 1
            request_id = self._request_id
            payload = {
                "jsonrpc": "2.0",
                "id": request_id,
                "method": method,
                "params": params,
            }
            self._process.stdin.write((json.dumps(payload) + "\n").encode())
            await self._process.stdin.drain()

            while True:
                line = await self._process.stdout.readline()
                if not line:
                    stderr = ""
                    if self._process.stderr:
                        stderr_bytes = await self._process.stderr.read()
                        stderr = stderr_bytes.decode(errors="replace")
                    raise RuntimeError(f"MCP process closed unexpectedly: {stderr}")

                message = json.loads(line.decode())
                if message.get("id") == request_id:
                    if "error" in message:
                        raise RuntimeError(message["error"].get("message", "MCP request failed"))
                    result = message.get("result")
                    if not isinstance(result, dict):
                        raise RuntimeError("Invalid MCP response payload")
                    return result
