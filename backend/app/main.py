from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.minio_utils import ensure_buckets
from .api import auth, health, user, resume, job, ats, interview, payments, admin, templates
from .core.logging import setup_logging
import logging

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
    logger.info("="*70)
    logger.info("🚀 Starting up AI Resume Agent...")
    logger.info("="*70)
    
    # Initialize MinIO bucket if needed
    try:
        logger.info("📦 Ensuring MinIO bucket exists...")
        ensure_buckets()
        logger.info("✅ MinIO bucket initialization complete")
    except Exception as e:
        logger.error(f"⚠️  MinIO initialization failed: {e}")
        logger.error("Resume uploads may fail. Check MinIO configuration and connectivity.")
    
    logger.info("✅ Startup complete - AI Resume Agent is ready")
    logger.info("="*70)

@app.on_event("shutdown")
async def shutdown():
    """Clean up on shutdown."""
    logger.info("🛑 Shutting down AI Resume Agent...")

