"""Base MCP provider interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProviderStatus:
    """Connection status for an MCP provider."""

    connected: bool
    provider: str
    message: str
    tools: list[str] = field(default_factory=list)


class MCPProvider(ABC):
    """Abstract provider for Cursor MCP connectivity."""

    name: str = "base"

    @abstractmethod
    async def connect(self) -> None:
        """Establish provider connection."""

    @abstractmethod
    async def disconnect(self) -> None:
        """Close provider connection."""

    @abstractmethod
    async def list_tools(self) -> list[dict[str, Any]]:
        """Return available MCP tools."""

    @abstractmethod
    async def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        """Invoke an MCP tool by name."""

    @abstractmethod
    async def health_check(self) -> ProviderStatus:
        """Return provider health and discovered tools."""
