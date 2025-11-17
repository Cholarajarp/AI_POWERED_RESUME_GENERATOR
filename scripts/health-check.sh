#!/usr/bin/env bash
set -e

echo "🔍 AI Resume Agent - System Health Check"
echo "========================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_pass() {
    echo -e "${GREEN}✅ $1${NC}"
}

check_fail() {
    echo -e "${RED}❌ $1${NC}"
}

check_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check Docker
echo "Checking Docker..."
if ! command -v docker &> /dev/null; then
    check_fail "Docker not installed"
    exit 1
fi
check_pass "Docker installed"

# Check Docker Compose
echo "Checking Docker Compose..."
if ! command -v docker compose &> /dev/null; then
    check_fail "Docker Compose not installed"
    exit 1
fi
check_pass "Docker Compose installed"

# Check .env file
echo ""
echo "Checking .env file..."
if [ ! -f .env ]; then
    check_fail ".env file not found"
    echo "Create it with: cp .env.example .env"
    exit 1
fi
check_pass ".env file exists"

# Check required env vars
echo ""
echo "Checking required environment variables..."
required_vars=("DATABASE_URL" "SECRET_KEY")
for var in "${required_vars[@]}"; do
    if grep -q "^$var=" .env; then
        check_pass "$var is set"
    else
        check_warn "$var is not set (may use default)"
    fi
done

# Check containers are running
echo ""
echo "Checking Docker containers..."
services=("ai-resume-db" "ai-resume-redis" "ai-resume-minio" "ai-resume-backend" "ai-resume-frontend")

for service in "${services[@]}"; do
    if docker ps -a --format '{{.Names}}' | grep -q "^${service}$"; then
        status=$(docker ps -a --filter "name=${service}" --format '{{.State}}')
        if [ "$status" = "running" ]; then
            check_pass "$service is running"
        else
            check_warn "$service exists but is $status"
        fi
    else
        check_warn "$service not created (run 'docker compose up --build -d')"
    fi
done

# Health checks for running services
echo ""
echo "Checking service health..."

# Database
if docker ps --format '{{.Names}}' | grep -q "ai-resume-db"; then
    if docker compose exec -T db pg_isready -U postgres &> /dev/null; then
        check_pass "PostgreSQL is responding"
    else
        check_fail "PostgreSQL is not responding"
    fi
fi

# Redis
if docker ps --format '{{.Names}}' | grep -q "ai-resume-redis"; then
    if docker compose exec -T redis redis-cli ping &> /dev/null; then
        check_pass "Redis is responding"
    else
        check_fail "Redis is not responding"
    fi
fi

# MinIO
if docker ps --format '{{.Names}}' | grep -q "ai-resume-minio"; then
    if docker compose exec -T minio curl -s http://localhost:9000/minio/health/live &> /dev/null; then
        check_pass "MinIO is responding"
    else
        check_fail "MinIO is not responding"
    fi
fi

# Backend API
echo ""
echo "Checking API endpoints..."
if curl -s http://localhost:8000/health &> /dev/null; then
    check_pass "Backend API is responding (http://localhost:8000)"
else
    check_warn "Backend API not responding at http://localhost:8000"
    check_warn "Make sure: docker compose logs -f backend"
fi

# Frontend
if curl -s http://localhost:3000 &> /dev/null; then
    check_pass "Frontend is responding (http://localhost:3000)"
else
    check_warn "Frontend not responding at http://localhost:3000"
fi

# Summary
echo ""
echo "========================================"
echo "🎯 Health check complete!"
echo ""
echo "📋 Quick reference:"
echo "  - Frontend: http://localhost:3000"
echo "  - API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - MinIO: http://localhost:9001"
echo ""
echo "📚 Commands:"
echo "  docker compose up --build -d      # Start all services"
echo "  docker compose logs -f backend    # Watch backend logs"
echo "  docker compose down -v            # Stop and clean up"
echo ""
echo "❓ Need help? Check docs/QUICKSTART.md"
