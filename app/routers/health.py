"""
Health check endpoints
"""

from fastapi import APIRouter
from app.data.catalog import CATALOG_STATS
from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "model": settings.MODEL_NAME,
        "catalog": CATALOG_STATS,
    }
