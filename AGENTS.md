# Agent guide — Company Brain

## Canonical event model (frozen root)

The system’s unit of recorded knowledge is the **Event**, defined only in:

- `contracts/event_schema.json` — JSON Schema (do not add or rename root fields)
- `backend/app/models/event.py` — `Event` and `EventMetadata` (must mirror the contract)

### Root fields (required)

`event_id`, `content`, `raw_type`, `event_type`, `timestamp`, `metadata`

**Semantic `event_type` values:** `message`, `decision`, `task`, `question`, `document`

### Structured `metadata` (required object)

| Field | Required | Notes |
|-------|----------|--------|
| `source` | Yes | `slack`, `email`, `calendar`, `jira`, `github`, `manual` |
| `channel` | No | e.g. Slack channel name (max 255 chars) |
| `tags` | No | String array; may be empty or omitted |

`metadata` uses `additionalProperties: false`. **Do not use metadata as a dumping ground** for fields that belong on the event root (`content`, `event_type`, etc.) or in separate domain models (processes, automations, RAG chunks).

### Adding new structured data

Before putting anything in `metadata`:

1. Is it **provenance or labeling** (source context, channel, tags)? → May belong in `metadata` only after updating the contract and `EventMetadata`.
2. Is it **core event meaning**? → Belongs in root fields (`content`, `raw_type`, `event_type`) — requires a formal schema change (rare; frozen).
3. Is it **feature-specific state** (workflow id, embedding id, automation run)? → Separate table/model; reference via `event_id`, not new metadata keys.

**Ingestion entrypoint:** `POST /ingest` → persists under `data/processed/events/`

### Building on top of events

| Area | Approach |
|------|----------|
| Process mining | Analyze stored `Event` streams; link processes via separate entities + `event_id` |
| Automation | Triggers/actions consume `Event`; workflow state outside the event |
| RAG | Chunk/embed `content`; vector/chunk records reference `event_id` |

Do not change root event fields or add parallel event types. Extend the platform around `Event`, not by forking the shape or overloading `metadata`.
