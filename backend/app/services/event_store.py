"""Persist ingested events to the local data directory."""
from __future__ import annotations

import json
from pathlib import Path

from app.core.config import settings
from app.models.event import Event


class EventStore:
    """File-backed event storage."""

    def __init__(self, events_dir: Path | None = None) -> None:
        self.events_dir = events_dir or settings.EVENTS_DIR
        self.events_dir.mkdir(parents=True, exist_ok=True)

    def _path_for(self, event_id: str) -> Path:
        return self.events_dir / f"{event_id}.json"

    def exists(self, event_id: str) -> bool:
        return self._path_for(event_id).is_file()

    def save(self, event: Event) -> None:
        path = self._path_for(event.event_id)
        payload = event.model_dump(mode="json")
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def get(self, event_id: str) -> Event | None:
        path = self._path_for(event_id)
        if not path.is_file():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return Event.model_validate(data)


event_store = EventStore()
