"""Cursor Bridge service layer."""

from __future__ import annotations

import time
import uuid
from typing import Any

from app.bridge.models import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatMessage,
    ToolCallRequest,
    ToolCallResponse,
)
from app.core.config import settings
from app.providers.base import MCPProvider, ProviderStatus
from app.providers.cursor_stdio import CursorStdioMCPProvider
from app.providers.mock import MockMCPProvider


class CursorBridgeService:
    """Orchestrates MCP providers and exposes bridge operations."""

    def __init__(self) -> None:
        self._provider: MCPProvider | None = None

    def _build_provider(self) -> MCPProvider:
        if settings.CURSOR_BRIDGE_BACKEND == "cursor-mcp":
            return CursorStdioMCPProvider(
                command=settings.CURSOR_MCP_COMMAND,
                args=settings.cursor_mcp_args_list,
                cwd=str(settings.PROJECT_ROOT),
            )
        return MockMCPProvider()

    async def get_provider(self) -> MCPProvider:
        if self._provider is None:
            self._provider = self._build_provider()
            await self._provider.connect()
        return self._provider

    async def shutdown(self) -> None:
        if self._provider is not None:
            await self._provider.disconnect()
            self._provider = None

    async def status(self) -> ProviderStatus:
        provider = await self.get_provider()
        return await provider.health_check()

    async def list_tools(self) -> list[dict[str, Any]]:
        provider = await self.get_provider()
        return await provider.list_tools()

    async def call_tool(self, request: ToolCallRequest) -> ToolCallResponse:
        provider = await self.get_provider()
        result = await provider.call_tool(request.name, request.arguments)
        return ToolCallResponse(name=request.name, result=result)

    async def chat_completion(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        user_message = _extract_user_message(request.messages)
        provider = await self.get_provider()

        if settings.CURSOR_BRIDGE_BACKEND == "mock":
            content = f"[mock-bridge:{request.model}] {user_message or 'Hello from Company Brain'}"
        else:
            tool_result = await provider.call_tool(
                "bridge_chat",
                {"message": user_message},
            )
            content = _content_to_text(tool_result.get("content", [])) or user_message

        return ChatCompletionResponse(
            id=f"chatcmpl-{uuid.uuid4().hex[:12]}",
            created=int(time.time()),
            model=request.model,
            choices=[
                {
                    "index": 0,
                    "message": ChatMessage(role="assistant", content=content),
                    "finish_reason": "stop",
                }
            ],
        )

    def list_models(self) -> list[dict[str, str]]:
        return [
            {"id": model, "object": "model", "owned_by": "cursor-bridge"}
            for model in settings.cursor_bridge_models_list
        ]


def _extract_user_message(messages: list[ChatMessage]) -> str:
    for message in reversed(messages):
        if message.role == "user" and message.content:
            if isinstance(message.content, str):
                return message.content
            if isinstance(message.content, list):
                parts: list[str] = []
                for part in message.content:
                    if isinstance(part, dict) and part.get("type") == "text":
                        parts.append(str(part.get("text", "")))
                return " ".join(parts).strip()
    return ""


def _content_to_text(content: list[Any]) -> str:
    parts: list[str] = []
    for item in content:
        if isinstance(item, dict) and item.get("type") == "text":
            parts.append(str(item.get("text", "")))
    return "\n".join(parts).strip()


bridge_service = CursorBridgeService()
