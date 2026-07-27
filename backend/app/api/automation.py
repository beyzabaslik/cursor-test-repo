"""Automation API endpoints"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/automation", tags=["automation"])


@router.post("/trigger")
async def trigger_automation(automation_id: str, payload: dict):
    """Trigger an automation"""
    return {"automation_id": automation_id, "status": "triggered", "payload": payload}


@router.get("/list")
async def list_automations():
    """List all automations"""
    return {"automations": []}
