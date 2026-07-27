"""Message model"""
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Message(BaseModel):
    """Message data model"""
    id: str
    content: str
    sender_id: str
    sender_name: str
    timestamp: datetime
    channel: Optional[str] = None
    thread_id: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "msg_123",
                "content": "Hello, how can I help?",
                "sender_id": "user_456",
                "sender_name": "John Doe",
                "timestamp": "2026-06-03T10:00:00Z",
                "channel": "general",
                "thread_id": None
            }
        }
