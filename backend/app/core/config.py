import os
import sys
from pydantic import BaseSettings, validator, Field
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    """Configuration with strict validation for required environment variables."""
    
    # Core database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    SECRET_KEY: str = Field("changeme-dev-only", env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(7, env="REFRESH_TOKEN_EXPIRE_DAYS")

    # LLM / OpenAI
    LLM_PROVIDER: str = Field("openai", env="LLM_PROVIDER")
    OPENAI_API_KEY: Optional[str] = Field(None, env="OPENAI_API_KEY")

    # Payment
    STRIPE_API_KEY: Optional[str] = Field(None, env="STRIPE_API_KEY")
    STRIPE_WEBHOOK_SECRET: Optional[str] = Field(None, env="STRIPE_WEBHOOK_SECRET")

    # MinIO (required for uploads)
    MINIO_ENDPOINT: str = Field("minio:9000", env="MINIO_ENDPOINT")
    MINIO_ACCESS_KEY: str = Field("miniouser", env="MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY: str = Field("miniosecret", env="MINIO_SECRET_KEY")
    MINIO_BUCKET: str = Field("resumes", env="MINIO_BUCKET")

    # Celery / Redis
    CELERY_BROKER: str = Field("redis://redis:6379/0", env="CELERY_BROKER")
    CELERY_BACKEND: str = Field("redis://redis:6379/1", env="CELERY_BACKEND")

    # App config
    DEBUG: bool = Field(False, env="DEBUG")
    ENVIRONMENT: str = Field("development", env="ENVIRONMENT")
    
    FRONTEND_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"]
    CORS_ORIGINS: List[str] = ["*"]

    # OAuth
    GOOGLE_OAUTH_CLIENT_ID: Optional[str] = Field(None, env="GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET: Optional[str] = Field(None, env="GOOGLE_OAUTH_CLIENT_SECRET")
    
    GITHUB_CLIENT_ID: Optional[str] = Field(None, env="GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET: Optional[str] = Field(None, env="GITHUB_CLIENT_SECRET")
    
    FRONTEND_URL: str = Field("http://localhost:3000", env="FRONTEND_URL")

    @validator('DATABASE_URL')
    def validate_database_url(cls, v):
        """Validate DATABASE_URL format."""
        if not v:
            raise ValueError('DATABASE_URL is required and cannot be empty')
        if not v.startswith(('postgresql://', 'postgresql+asyncpg://', 'sqlite://')):
            raise ValueError('DATABASE_URL must be a valid PostgreSQL or SQLite URL, got: ' + v[:50])
        return v

    @validator('MINIO_ENDPOINT')
    def validate_minio_endpoint(cls, v):
        """Validate MinIO endpoint."""
        if not v:
            raise ValueError('MINIO_ENDPOINT is required')
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True

def _load_settings():
    """Load and validate settings, exit with clear error if validation fails."""
    try:
        settings = Settings()
        logger.info(f"✅ Settings loaded successfully (environment: {settings.ENVIRONMENT})")
        return settings
    except Exception as e:
        print("\n" + "="*70)
        print("❌ CONFIGURATION ERROR - Missing or Invalid Environment Variables")
        print("="*70)
        print(f"\nError: {e}\n")
        print("REQUIRED variables (must be set in .env file):")
        print("  • DATABASE_URL       - PostgreSQL connection string")
        print("  • MINIO_ENDPOINT     - MinIO server address (default: minio:9000)")
        print("  • MINIO_ACCESS_KEY   - MinIO access key (default: miniouser)")
        print("  • MINIO_SECRET_KEY   - MinIO secret key (default: miniosecret)")
        print("\nOPTIONAL variables (for specific features):")
        print("  • OPENAI_API_KEY     - For AI resume/interview features")
        print("  • STRIPE_API_KEY     - For payment processing")
        print("  • GOOGLE_OAUTH_CLIENT_ID/SECRET - For Google OAuth login")
        print("  • GITHUB_CLIENT_ID/SECRET - For GitHub OAuth login")
        print("\nQuick fix:")
        print("  1. Copy .env.example to .env:  cp .env.example .env")
        print("  2. Fill in required values in .env")
        print("  3. Restart the application")
        print("="*70 + "\n")
        sys.exit(1)

settings = _load_settings()
