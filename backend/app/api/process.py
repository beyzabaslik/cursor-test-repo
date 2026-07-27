"""Data processing API endpoints"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/process", tags=["process"])


@router.post("/start")
async def start_process(process_id: str):
    """Start a processing job"""
    return {"process_id": process_id, "status": "started"}


@router.get("/status/{process_id}")
async def get_process_status(process_id: str):
    """Get processing job status"""
    return {"process_id": process_id, "status": "running"}
