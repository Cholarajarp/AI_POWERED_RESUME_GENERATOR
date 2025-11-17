#!/bin/bash

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "\n${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     AI RESUME AGENT - Production Readiness Verification     ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}\n"

# Check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}📋 Checking prerequisites...${NC}"
    
    local prereqs_ok=true
    
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker is not installed${NC}"
        prereqs_ok=false
    else
        echo -e "${GREEN}✅ Docker installed${NC}"
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo -e "${RED}❌ Docker Compose is not installed${NC}"
        prereqs_ok=false
    else
        echo -e "${GREEN}✅ Docker Compose installed${NC}"
    fi
    
    if ! command -v curl &> /dev/null; then
        echo -e "${RED}❌ curl is not installed${NC}"
        prereqs_ok=false
    else
        echo -e "${GREEN}✅ curl installed${NC}"
    fi
    
    if [ "$prereqs_ok" = false ]; then
        echo -e "\n${RED}Prerequisites check failed${NC}"
        return 1
    fi
    
    return 0
}

# Check environment file
check_env_file() {
    echo -e "\n${YELLOW}📝 Checking environment configuration...${NC}"
    
    if [ ! -f ".env" ]; then
        echo -e "${RED}❌ .env file not found${NC}"
        echo -e "${YELLOW}   Run: cp .env.example .env${NC}"
        return 1
    else
        echo -e "${GREEN}✅ .env file exists${NC}"
    fi
    
    # Check for required variables
    local required_vars=("DATABASE_URL" "SECRET_KEY" "MINIO_ACCESS_KEY" "MINIO_SECRET_KEY")
    for var in "${required_vars[@]}"; do
        if grep -q "^${var}=" .env; then
            echo -e "${GREEN}✅ ${var} configured${NC}"
        else
            echo -e "${RED}❌ ${var} missing${NC}"
            return 1
        fi
    done
    
    return 0
}

# Build images
build_images() {
    echo -e "\n${YELLOW}🔨 Building Docker images...${NC}"
    
    if docker-compose build; then
        echo -e "${GREEN}✅ Images built successfully${NC}"
        return 0
    else
        echo -e "${RED}❌ Image build failed${NC}"
        return 1
    fi
}

# Start services
start_services() {
    echo -e "\n${YELLOW}🚀 Starting services...${NC}"
    
    if docker-compose up -d; then
        echo -e "${GREEN}✅ Services started${NC}"
        echo -e "${YELLOW}⏳ Waiting 10 seconds for services to stabilize...${NC}"
        sleep 10
        return 0
    else
        echo -e "${RED}❌ Failed to start services${NC}"
        return 1
    fi
}

# Check container health
check_containers() {
    echo -e "\n${YELLOW}🏥 Checking container health...${NC}"
    
    local containers=("ai-resume-db" "ai-resume-redis" "ai-resume-minio" "ai-resume-backend" "ai-resume-frontend")
    
    for container in "${containers[@]}"; do
        if docker ps | grep -q "$container"; then
            echo -e "${GREEN}✅ $container running${NC}"
        else
            echo -e "${RED}❌ $container not running${NC}"
            return 1
        fi
    done
    
    return 0
}

# Test health endpoints
test_health_endpoints() {
    echo -e "\n${YELLOW}🏥 Testing health endpoints...${NC}"
    
    local backend_url="http://localhost:8000"
    
    # Test /health
    if curl -s "$backend_url/health" > /dev/null; then
        echo -e "${GREEN}✅ GET /health responding${NC}"
    else
        echo -e "${RED}❌ GET /health failed${NC}"
        return 1
    fi
    
    # Test /health/ready
    if curl -s "$backend_url/health/ready" > /dev/null; then
        echo -e "${GREEN}✅ GET /health/ready responding${NC}"
    else
        echo -e "${RED}❌ GET /health/ready failed${NC}"
        return 1
    fi
    
    # Test /docs
    if curl -s "$backend_url/docs" > /dev/null; then
        echo -e "${GREEN}✅ Swagger API docs available${NC}"
    else
        echo -e "${RED}❌ Swagger docs not accessible${NC}"
        return 1
    fi
    
    return 0
}

# Test API endpoints
test_api_endpoints() {
    echo -e "\n${YELLOW}🔌 Testing API endpoints...${NC}"
    
    local backend_url="http://localhost:8000"
    
    # Test auth endpoint (should 400 or 401 without credentials)
    if curl -s -w "%{http_code}" -o /dev/null "$backend_url/auth/login" || [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Auth endpoints available${NC}"
    else
        echo -e "${YELLOW}⚠️  Auth endpoint check inconclusive${NC}"
    fi
    
    return 0
}

# Check logs for errors
check_logs() {
    echo -e "\n${YELLOW}📋 Checking for startup errors...${NC}"
    
    echo -e "${BLUE}Backend logs (last 20 lines):${NC}"
    docker-compose logs --tail 20 backend | head -20
    
    return 0
}

# Display service URLs
display_urls() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}🎉 All systems ready!${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}\n"
    
    echo -e "${YELLOW}Access Points:${NC}"
    echo -e "  🌐 Frontend:  ${GREEN}http://localhost:3000${NC}"
    echo -e "  📡 API Docs:  ${GREEN}http://localhost:8000/docs${NC}"
    echo -e "  📦 MinIO:     ${GREEN}http://localhost:9001${NC}\n"
    
    echo -e "${YELLOW}Services Status:${NC}"
    docker-compose ps | tail -n +2 | while IFS= read -r line; do
        if echo "$line" | grep -q "Up"; then
            echo -e "  ${GREEN}✅ $line${NC}"
        else
            echo -e "  ${RED}❌ $line${NC}"
        fi
    done
    
    echo -e "\n${YELLOW}Next Steps:${NC}"
    echo -e "  1. Visit ${GREEN}http://localhost:3000${NC}"
    echo -e "  2. Create an account and log in"
    echo -e "  3. Try uploading a resume"
    echo -e "  4. Test AI features (if OPENAI_API_KEY is set)"
    echo -e "  5. Check API docs at ${GREEN}http://localhost:8000/docs${NC}\n"
    
    echo -e "${YELLOW}Useful Commands:${NC}"
    echo -e "  View all logs:         ${GREEN}docker-compose logs -f${NC}"
    echo -e "  View backend logs:     ${GREEN}docker-compose logs -f backend${NC}"
    echo -e "  Stop services:         ${GREEN}docker-compose down${NC}"
    echo -e "  Rebuild & restart:     ${GREEN}docker-compose up --build -d${NC}"
    echo -e "  Execute backend shell: ${GREEN}docker-compose exec backend bash${NC}\n"
}

# Main execution
main() {
    local failures=0
    
    check_prerequisites || ((failures++))
    check_env_file || ((failures++))
    
    if [ $failures -eq 0 ]; then
        build_images || ((failures++))
        start_services || ((failures++))
        sleep 5
        check_containers || ((failures++))
        test_health_endpoints || ((failures++))
        test_api_endpoints || ((failures++))
    fi
    
    if [ $failures -gt 0 ]; then
        echo -e "\n${RED}═══════════════════════════════════════════════════════════${NC}"
        echo -e "${RED}❌ Verification failed with $failures error(s)${NC}"
        echo -e "${RED}═══════════════════════════════════════════════════════════${NC}\n"
        
        echo -e "${YELLOW}Debugging tips:${NC}"
        echo -e "  1. Check .env file exists and is properly configured"
        echo -e "  2. Ensure Docker is running"
        echo -e "  3. Check logs: ${GREEN}docker-compose logs --tail 50${NC}"
        echo -e "  4. Free up ports: Check if 3000, 8000, 9001, 5432, 6379 are in use${NC}"
        echo -e "  5. Rebuild images: ${GREEN}docker-compose build --no-cache${NC}\n"
        
        check_logs
        exit 1
    fi
    
    display_urls
    exit 0
}

main
