"""MinIO utilities for S3-compatible object storage."""

import logging
from minio import Minio
from minio.error import S3Error
from .config import settings

logger = logging.getLogger(__name__)


def get_minio_client() -> Minio:
    """Get MinIO client instance.
    
    Returns:
        Minio: Configured MinIO client
        
    Raises:
        Exception: If MinIO credentials are invalid
    """
    # Remove scheme from endpoint if present
    endpoint = settings.MINIO_ENDPOINT.replace("http://", "").replace("https://", "")
    
    client = Minio(
        endpoint=endpoint,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=False  # Use HTTP in dev; set True for production with HTTPS
    )
    return client


def ensure_buckets() -> None:
    """Ensure required MinIO buckets exist, create if missing.
    
    This function is called during app startup to ensure the MinIO bucket
    exists before any upload operations are attempted.
    
    Raises:
        S3Error: If bucket creation fails (permissions, connection, etc.)
    """
    try:
        client = get_minio_client()
        bucket_name = settings.MINIO_BUCKET
        
        # Check if bucket exists
        exists = client.bucket_exists(bucket_name)
        
        if exists:
            logger.info(f"✅ MinIO bucket exists: {bucket_name}")
        else:
            # Create bucket
            client.make_bucket(bucket_name)
            logger.info(f"✅ Created MinIO bucket: {bucket_name}")
            
    except S3Error as e:
        logger.error(f"❌ MinIO S3 error while ensuring bucket: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error while initializing MinIO: {e}")
        raise


def delete_object(bucket_name: str, object_name: str) -> bool:
    """Delete an object from MinIO.
    
    Args:
        bucket_name: Name of the bucket
        object_name: Path/name of the object to delete
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        client = get_minio_client()
        client.remove_object(bucket_name, object_name)
        logger.info(f"Deleted object: {bucket_name}/{object_name}")
        return True
    except S3Error as e:
        logger.error(f"Failed to delete object: {e}")
        return False


def upload_file(bucket_name: str, object_name: str, file_path: str) -> bool:
    """Upload a file to MinIO.
    
    Args:
        bucket_name: Name of the bucket
        object_name: Path/name for the object in bucket
        file_path: Local file path to upload
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        client = get_minio_client()
        client.fput_object(bucket_name, object_name, file_path)
        logger.info(f"Uploaded file: {bucket_name}/{object_name}")
        return True
    except S3Error as e:
        logger.error(f"Failed to upload file: {e}")
        return False


def get_presigned_url(bucket_name: str, object_name: str, expires: int = 3600) -> str:
    """Get a presigned URL for accessing an object.
    
    Args:
        bucket_name: Name of the bucket
        object_name: Path/name of the object
        expires: URL expiration time in seconds (default: 1 hour)
        
    Returns:
        str: Presigned URL for accessing the object
    """
    try:
        from datetime import timedelta
        client = get_minio_client()
        url = client.get_presigned_url(
            "GET",
            bucket_name,
            object_name,
            expires=timedelta(seconds=expires)
        )
        return url
    except S3Error as e:
        logger.error(f"Failed to generate presigned URL: {e}")
        raise
