"""Chat API endpoints"""
from fastapi import APIRouter, WebSocket

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time chat"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Process message and send response
            await websocket.send_text(f"Echo: {data}")
    except Exception as e:
        await websocket.close(code=1000)


@router.post("/message")
async def send_message(message: dict):
    """Send a chat message"""
    return {"status": "received", "message": message}
