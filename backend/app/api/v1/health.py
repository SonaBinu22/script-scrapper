from datetime import datetime, timezone
from fastapi import APIRouter, status
from backend.app.core.config import settings
from backend.app.database.connection import check_database_connectivity

router = APIRouter(tags=["Health & Diagnostics"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def get_health():
    """
    Lightweight liveness probe for reverse proxies and monitoring.
    Does not incur database queries.
    """
    return {
        "success": True,
        "data": {
            "status": "healthy",
            "service": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }


@router.get("/system/status", status_code=status.HTTP_200_OK)
async def get_system_status():
    """
    Comprehensive readiness and diagnostics probe.
    Tests active database connectivity and reports connection pool bounds.
    """
    db_status = await check_database_connectivity()

    return {
        "success": True,
        "data": {
            "status": "operational" if db_status["connected"] else "degraded",
            "environment": settings.ENVIRONMENT,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "database": db_status,
            "server": {
                "configured_workers": settings.UVICORN_WORKERS,
                "per_worker_pool_max": settings.DB_POOL_SIZE + settings.DB_MAX_OVERFLOW,
                "aggregate_api_peak_ceiling": settings.UVICORN_WORKERS * (
                    settings.DB_POOL_SIZE + settings.DB_MAX_OVERFLOW
                ),
            },
        },
    }
