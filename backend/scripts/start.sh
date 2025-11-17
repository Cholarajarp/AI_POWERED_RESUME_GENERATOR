#!/usr/bin/env bash
set -e

echo "🚀 Starting AI Resume Agent Backend..."

# Wait for database
echo "⏳ Waiting for database..."
while ! pg_isready -h db -U postgres; do
  sleep 1
done
echo "✅ Database is ready"

# Wait for Redis
echo "⏳ Waiting for Redis..."
while ! redis-cli -h redis ping > /dev/null 2>&1; do
  sleep 1
done
echo "✅ Redis is ready"

# Wait for MinIO
echo "⏳ Waiting for MinIO..."
while ! curl -f http://minio:9000/minio/health/live > /dev/null 2>&1; do
  sleep 1
done
echo "✅ MinIO is ready"

# Run database migrations
echo "🔧 Running database migrations..."
cd /app
alembic upgrade head
echo "✅ Migrations complete"

# Start the application
echo "🎯 Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
