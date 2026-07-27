"""Process model"""
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class ProcessStatus(str, Enum):
    """Process status enum"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Process(BaseModel):
    """Process data model"""
    id: str
    name: str
    description: Optional[str] = None
    status: ProcessStatus = ProcessStatus.PENDING
    created_at: datetime
    updated_at: datetime
    owner_id: str
    steps: List[dict] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "proc_123",
                "name": "Data Processing",
                "description": "Process raw data",
                "status": "running",
                "created_at": "2026-06-03T10:00:00Z",
                "updated_at": "2026-06-03T10:30:00Z",
                "owner_id": "user_456",
                "steps": []
            }
        }
