from fastapi import APIRouter, status
from datetime import datetime
from typing import Dict, Any

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Book Scraping API",
        "version": "1.0.0"
    }
