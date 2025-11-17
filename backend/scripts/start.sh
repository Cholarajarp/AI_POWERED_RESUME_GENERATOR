#!/bin/bash
set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Helper function to wait for service
wait_for() {
  local host="$1"
  local port="$2"
  local service_name="${3:-$host}"
  local max_retries=30
  local retry_count=0
  
  echo -e "${YELLOW}⏳ Waiting for $service_name ($host:$port)...${NC}"
  
  while ! nc -z "$host" "$port" >/dev/null 2>&1; do
    retry_count=$((retry_count + 1))
    if [ $retry_count -ge $max_retries ]; then
      echo -e "${RED}❌ Failed to connect to $service_name after $max_retries attempts${NC}"
      exit 1
    fi
    sleep 1
  done
  
  echo -e "${GREEN}✅ $service_name is ready${NC}"
}

echo -e "${YELLOW}🚀 Starting AI Resume Agent Backend...${NC}\n"

# Wait for PostgreSQL
wait_for db 5432 "PostgreSQL"

# Wait for Redis
wait_for redis 6379 "Redis"

# Wait for MinIO
wait_for minio 9000 "MinIO"

# Run database migrations
echo -e "\n${YELLOW}📊 Running Alembic migrations...${NC}"
cd /app
if ! alembic upgrade head; then
  echo -e "${RED}❌ Alembic migration failed${NC}"
  exit 1
fi
echo -e "${GREEN}✅ Migrations completed${NC}"

# Create admin user if environment variable is set
if [ "${CREATE_ADMIN_ON_START:-0}" = "1" ]; then
  echo -e "\n${YELLOW}👤 Creating admin user...${NC}"
  ADMIN_EMAIL="${ADMIN_EMAIL:-admin@example.com}"
  ADMIN_PASSWORD="${ADMIN_PASSWORD:-changeme}"
  
  if [ -f "scripts/create_admin.py" ]; then
    python scripts/create_admin.py \
      --email "$ADMIN_EMAIL" \
      --password "$ADMIN_PASSWORD" \
      --name "Admin User" || echo -e "${YELLOW}⚠️  Admin creation skipped or already exists${NC}"
  else
    echo -e "${YELLOW}⚠️  create_admin.py not found, skipping admin creation${NC}"
  fi
fi

# Start the application
echo -e "\n${GREEN}🎯 Starting FastAPI application...${NC}"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level info
