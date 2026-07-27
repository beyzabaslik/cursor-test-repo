"""Mock MCP provider for local demo and tests."""

from __future__ import annotations

from typing import Any

from app.providers.base import MCPProvider, ProviderStatus


class MockMCPProvider(MCPProvider):
    """Deterministic MCP provider that does not require Cursor."""

    name = "mock"

    _TOOLS: list[dict[str, Any]] = [
        {
            "name": "get_context_index",
            "description": "Discover available Cursor rules, agents, and skills.",
            "inputSchema": {"type": "object", "properties": {}},
        },
        {
            "name": "get_active_rules",
            "description": "Return rules active for the current task context.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "paths": {"type": "array", "items": {"type": "string"}},
                    "task": {"type": "string"},
                },
            },
        },
        {
            "name": "bridge_chat",
            "description": "Return a demo chat completion through the bridge.",
            "inputSchema": {
                "type": "object",
                "properties": {"message": {"type": "string"}},
                "required": ["message"],
            },
        },
    ]

    def __init__(self) -> None:
        self._connected = False

    async def connect(self) -> None:
        self._connected = True

    async def disconnect(self) -> None:
        self._connected = False

    async def list_tools(self) -> list[dict[str, Any]]:
        return list(self._TOOLS)

    async def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        if not self._connected:
            await self.connect()

        args = arguments or {}
        if name == "get_context_index":
            return {
                "content": [
                    {
                        "type": "text",
                        "text": '{"rules":["company-brain-demo"],"agents":["cursor-bridge"],"skills":[]}',
                    }
                ],
                "isError": False,
            }
        if name == "get_active_rules":
            task = args.get("task", "Company Brain demo")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f'Active rules for "{task}": use Cursor Bridge provider layer.',
                    }
                ],
                "isError": False,
            }
        if name == "bridge_chat":
            message = args.get("message", "")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"[mock-bridge] Received: {message}",
                    }
                ],
                "isError": False,
            }
        return {
            "content": [{"type": "text", "text": f"Unknown mock tool: {name}"}],
            "isError": True,
        }

    async def health_check(self) -> ProviderStatus:
        tools = await self.list_tools()
        return ProviderStatus(
            connected=self._connected,
            provider=self.name,
            message="Mock MCP provider ready",
            tools=[tool["name"] for tool in tools],
        )
