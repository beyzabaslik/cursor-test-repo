"""Provider layer tests."""

import pytest

from app.providers.mock import MockMCPProvider


@pytest.mark.asyncio
async def test_mock_provider_lists_tools():
    provider = MockMCPProvider()
    await provider.connect()
    tools = await provider.list_tools()
    assert len(tools) >= 3


@pytest.mark.asyncio
async def test_mock_provider_calls_bridge_chat():
    provider = MockMCPProvider()
    result = await provider.call_tool("bridge_chat", {"message": "ping"})
    assert result["isError"] is False
    assert "ping" in result["content"][0]["text"]
