"""Health check endpoints for monitoring application and service dependencies."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", tags=["health"])
@router.get("", tags=["health"])
async def health_check():
    """Main health check endpoint - returns OK if app is running."""
    return JSONResponse(
        status_code=200,
        content={
            "status": "ok",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "AI Resume Agent"
        }
    )


@router.get("/ready", tags=["health"])
async def ready():
    """Readiness probe - checks if app is ready to serve requests.
    
    Performs checks on:
    - Database connectivity
    - MinIO/S3 storage
    - Redis cache (if used)
    """
    checks = {
        "database": await check_database(),
        "minio": await check_minio(),
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # All checks must pass for readiness
    all_ready = all(checks.values())
    
    if not all_ready:
        logger.warning(f"Readiness check failed: {checks}")
        raise HTTPException(
            status_code=503,
            detail="Service not ready - some dependencies failed"
        )
    
    return JSONResponse(
        status_code=200,
        content={"status": "ready", **checks}
    )


@router.get("/live", tags=["health"])
async def live():
    """Liveness probe - returns OK if container is alive."""
    return JSONResponse(
        status_code=200,
        content={
            "status": "alive",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@router.get("/detailed", tags=["health"])
async def detailed_health():
    """Detailed health check with all service statuses."""
    return JSONResponse(
        status_code=200,
        content={
            "status": "ok",
            "database": await check_database(),
            "minio": await check_minio(),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


async def check_database() -> bool:
    """Check database connectivity.
    
    Returns:
        bool: True if database is accessible, False otherwise
    """
    try:
        from sqlalchemy import text
        from app.core.config import settings
        import asyncpg
        
        # Create async connection to test database
        conn = await asyncpg.connect(
            settings.DATABASE_URL.replace("+asyncpg", "").replace("postgresql", "postgresql+asyncpg")
        )
        await conn.execute("SELECT 1")
        await conn.close()
        
        logger.debug("✅ Database check passed")
        return True
    except Exception as e:
        logger.error(f"❌ Database check failed: {e}")
        return False


async def check_minio() -> bool:
    """Check MinIO/S3 storage connectivity.
    
    Returns:
        bool: True if MinIO is accessible, False otherwise
    """
    try:
        from app.core.minio_utils import get_minio_client
        from app.core.config import settings
        
        client = get_minio_client()
        # Check if bucket exists (this tests connectivity)
        client.bucket_exists(settings.MINIO_BUCKET)
        
        logger.debug("✅ MinIO check passed")
        return True
    except Exception as e:
        logger.error(f"❌ MinIO check failed: {e}")
        return False

