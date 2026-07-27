"""Cursor Bridge tests."""

from httpx import ASGITransport, AsyncClient
import pytest

from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client


@pytest.mark.asyncio
async def test_bridge_health(client):
    response = await client.get("/api/cursor-bridge/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["backend"] == "mock"
    assert payload["provider"] == "mock"


@pytest.mark.asyncio
async def test_bridge_tools(client):
    response = await client.get("/api/cursor-bridge/tools")
    assert response.status_code == 200
    tools = response.json()["tools"]
    assert any(tool["name"] == "get_context_index" for tool in tools)


@pytest.mark.asyncio
async def test_bridge_chat_completion(client):
    response = await client.post(
        "/api/cursor-bridge/v1/chat/completions",
        headers={"Authorization": "Bearer sk-curbr-local-dev"},
        json={
            "model": "cursor-fast",
            "messages": [{"role": "user", "content": "Hello bridge"}],
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["choices"][0]["message"]["content"].startswith("[mock-bridge:cursor-fast]")


@pytest.mark.asyncio
async def test_bridge_tool_call(client):
    response = await client.post(
        "/api/cursor-bridge/tools/call",
        json={"name": "get_active_rules", "arguments": {"task": "demo"}},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "get_active_rules"
    assert payload["result"]["isError"] is False
