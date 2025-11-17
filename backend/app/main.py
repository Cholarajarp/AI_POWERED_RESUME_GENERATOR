from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api import auth, health, user, resume, job, ats, interview, payments, admin, templates
from .core.logging import setup_logging
import logging
import os

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Interview & Resume Agent",
    description="AI-powered resume and interview preparation platform",
    version="1.0.0"
)

# Configure CORS with proper origin handling
cors_origins = settings.FRONTEND_ORIGINS if settings.ENVIRONMENT == "development" else [settings.FRONTEND_URL]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=600,
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"]) 
app.include_router(resume.router, prefix="/resume", tags=["resume"])
app.include_router(job.router, prefix="/job", tags=["job"])
app.include_router(ats.router, prefix="/ats", tags=["ats"])
app.include_router(interview.router, prefix="/interview", tags=["interview"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])
app.include_router(templates.router, prefix="/templates", tags=["templates"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

@app.on_event("startup")
async def startup():
    """Initialize app on startup: DB pools, MinIO bucket, etc."""
    logger.info("Starting up AI Resume Agent...")
    
    # Initialize MinIO bucket if needed
    try:
        from minio import Minio
        minio_client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False
        )
        if not minio_client.bucket_exists(settings.MINIO_BUCKET):
            minio_client.make_bucket(settings.MINIO_BUCKET)
            logger.info(f"Created MinIO bucket: {settings.MINIO_BUCKET}")
        else:
            logger.info(f"MinIO bucket exists: {settings.MINIO_BUCKET}")
    except Exception as e:
        logger.warning(f"MinIO initialization warning: {e}")
    
    logger.info("Startup complete")

@app.on_event("shutdown")
async def shutdown():
    """Clean up on shutdown."""
    logger.info("Shutting down AI Resume Agent...")
