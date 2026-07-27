"""FastAPI application entry point"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import automation, chat, cursor_bridge, ingest, process
from app.bridge.service import bridge_service
from app.core.config import settings

app = FastAPI(
    title="Company Brain API",
    description="Enterprise knowledge management and automation platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ingest.events_router)
app.include_router(ingest.legacy_router)
app.include_router(chat.router)
app.include_router(process.router)
app.include_router(automation.router)
app.include_router(cursor_bridge.router)

_frontend_root = Path(__file__).resolve().parents[2] / "frontend"
if _frontend_root.exists():
    app.mount("/demo", StaticFiles(directory=str(_frontend_root), html=True), name="demo")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Company Brain API is running"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.on_event("shutdown")
async def shutdown_bridge() -> None:
    await bridge_service.shutdown()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT
    )
