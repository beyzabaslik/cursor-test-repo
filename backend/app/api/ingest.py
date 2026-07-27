"""Data ingestion API endpoints"""
from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.models.event import Event, EventIngestResponse
from app.services.event_store import event_store

events_router = APIRouter(tags=["ingest"])
legacy_router = APIRouter(prefix="/api/ingest", tags=["ingest"])


@events_router.post(
    "/ingest",
    response_model=EventIngestResponse,
    status_code=status.HTTP_201_CREATED,
)
async def ingest_event(event: Event) -> EventIngestResponse:
    """Accept and persist a single event (contracts/event_schema.json)."""
    if event_store.exists(event.event_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Event with event_id '{event.event_id}' already exists",
        )
    event_store.save(event)
    return EventIngestResponse(event_id=event.event_id)


@legacy_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload file for ingestion"""
    return {"filename": file.filename, "status": "uploaded"}


@legacy_router.post("/process")
async def process_data(data: dict):
    """Process ingested data"""
    return {"status": "processing", "data": data}
