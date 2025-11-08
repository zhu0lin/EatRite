"""Health check endpoints."""

from fastapi import APIRouter
from datetime import datetime, timezone


router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns the API status and current timestamp.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "EatRite API"
    }


