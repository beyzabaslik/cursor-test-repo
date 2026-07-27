"""Canonical Event model — mirrors contracts/event_schema.json (frozen root fields).

Process mining, automation, and RAG use this type. Metadata is structured and
closed; do not store core event data there or add keys without schema review.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class EventType(str, Enum):
    message = "message"
    decision = "decision"
    task = "task"
    question = "question"
    document = "document"


class EventSource(str, Enum):
    slack = "slack"
    email = "email"
    calendar = "calendar"
    jira = "jira"
    github = "github"
    manual = "manual"


class EventMetadata(BaseModel):
    """Structured metadata — provenance and labeling only."""

    model_config = ConfigDict(extra="forbid")

    source: EventSource
    channel: Optional[str] = Field(default=None, max_length=255)
    tags: list[str] = Field(default_factory=list)


class Event(BaseModel):
    """Event payload validated against event_schema.json"""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "event_id": "evt_123",
                "content": "Q4 planning meeting scheduled for Friday",
                "raw_type": "slack_message",
                "event_type": "message",
                "timestamp": "2026-06-03T10:00:00Z",
                "metadata": {
                    "source": "slack",
                    "channel": "planning",
                    "tags": ["planning", "q4"],
                },
            }
        },
    )

    event_id: str = Field(..., pattern=r"^evt_[a-zA-Z0-9_-]+$")
    content: str = Field(..., min_length=1, max_length=2000)
    raw_type: str = Field(..., min_length=1, max_length=128)
    event_type: EventType
    timestamp: datetime
    metadata: EventMetadata


class EventIngestResponse(BaseModel):
    event_id: str
    status: str = "ingested"
