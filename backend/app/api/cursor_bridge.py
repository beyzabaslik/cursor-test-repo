"""Local Cursor Bridge HTTP endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException, status
from fastapi.responses import JSONResponse

from app.bridge.models import ChatCompletionRequest, ToolCallRequest
from app.bridge.service import bridge_service
from app.core.config import settings

router = APIRouter(prefix="/api/cursor-bridge", tags=["cursor-bridge"])


def require_bridge_api_key(authorization: str | None = None, x_api_key: str | None = None) -> None:
    """Fail closed when a bridge API key is configured but missing/invalid."""
    expected = settings.CURSOR_BRIDGE_API_KEY
    if not expected:
        return

    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
    elif x_api_key:
        token = x_api_key.strip()

    if token != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Cursor Bridge API key",
        )


@router.get("/health")
async def bridge_health():
    """Public health endpoint for the local bridge."""
    status_payload = await bridge_service.status()
    return {
        "status": "healthy" if status_payload.connected else "degraded",
        "provider": status_payload.provider,
        "connected": status_payload.connected,
        "message": status_payload.message,
        "backend": settings.CURSOR_BRIDGE_BACKEND,
        "endpoint": settings.CURSOR_BRIDGE_PUBLIC_URL,
    }


@router.get("/status")
async def bridge_status():
    """Detailed bridge connection status."""
    status_payload = await bridge_service.status()
    return {
        "provider": status_payload.provider,
        "connected": status_payload.connected,
        "message": status_payload.message,
        "tools": status_payload.tools,
        "models": bridge_service.list_models(),
        "backend": settings.CURSOR_BRIDGE_BACKEND,
    }


@router.get("/tools")
async def list_tools():
    """List MCP tools exposed through the bridge."""
    return {"tools": await bridge_service.list_tools()}


@router.post("/tools/call")
async def call_tool(request: ToolCallRequest):
    """Call an MCP tool through the provider layer."""
    return await bridge_service.call_tool(request)


@router.get("/v1/models")
async def list_models(
    authorization: str | None = Header(default=None),
    x_api_key: str | None = Header(default=None, alias="x-api-key"),
):
    """OpenAI-compatible model listing."""
    require_bridge_api_key(authorization, x_api_key)
    return {"object": "list", "data": bridge_service.list_models()}


@router.post("/v1/chat/completions")
async def chat_completions(
    request: ChatCompletionRequest,
    authorization: str | None = Header(default=None),
    x_api_key: str | None = Header(default=None, alias="x-api-key"),
):
    """OpenAI-compatible chat completion endpoint backed by the bridge."""
    if not settings.CURSOR_BRIDGE_API_KEY:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"error": "configuration_error", "message": "CURSOR_BRIDGE_API_KEY is not set"},
        )

    require_bridge_api_key(authorization, x_api_key)

    if request.stream:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Streaming is not implemented in this demo bridge",
        )

    return await bridge_service.chat_completion(request)
