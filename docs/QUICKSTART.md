# Quick Start Guide

Get the AI Resume Agent running locally in 3 steps.

## Prerequisites

- Docker & Docker Compose installed
- Git
- `.env` file with required secrets

## Step 1: Create .env file

Copy the example and fill in your secrets:

```bash
cp .env.example .env
```

Edit `.env` and add:
```env
# Required
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/resume_agent_db
SECRET_KEY=your-super-secret-key-change-in-production

# Optional but recommended
OPENAI_API_KEY=sk-...
STRIPE_API_KEY=sk_live_...

# OAuth (optional)
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
GOOGLE_OAUTH_CLIENT_ID=...
GOOGLE_OAUTH_CLIENT_SECRET=...

# Environment
ENVIRONMENT=development
DEBUG=true
FRONTEND_URL=http://localhost:3000
```

## Step 2: Build and Start Containers

```bash
# Build images and start all services
docker compose up --build -d

# Watch logs (especially backend startup)
docker compose logs -f backend
```

Expected output:
```
backend  | ✅ Settings loaded successfully (environment: development)
backend  | ✅ Database is ready
backend  | ✅ Redis is ready
backend  | ✅ MinIO is ready
backend  | 🔧 Running database migrations...
backend  | ✅ Migrations complete
backend  | 🎯 Starting FastAPI application...
```

## Step 3: Access the App

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001 (user: `miniouser`, pass: `miniosecret`)

## Verify Everything Works

```bash
# Check health endpoint
curl http://localhost:8000/health

# Check database
docker compose exec db psql -U postgres -d resume_agent_db -c "SELECT 1"

# Check Redis
docker compose exec redis redis-cli ping

# Check MinIO (should output "true")
docker compose exec minio mc ls minio/resumes
```

## Troubleshooting

### Backend crashes on startup

Check logs:
```bash
docker compose logs backend --tail 50
```

Common issues:
- **Missing .env**: Create it with `cp .env.example .env`
- **Migration errors**: Check database connection string
- **Port conflict**: Ensure ports 8000, 3000, 5432 are free

### Frontend can't reach backend

**Problem**: CORS errors in browser console

**Solution**: Make sure backend is running and accessible:
```bash
curl http://localhost:8000/health
```

### Database connection refused

**Problem**: `could not connect to server`

**Solution**: Wait for postgres container to be healthy:
```bash
docker compose exec db pg_isready -U postgres
```

## Useful Commands

```bash
# View all container logs
docker compose logs -f

# Stop all services
docker compose down

# Stop and remove volumes (clean slate)
docker compose down -v

# Rebuild a specific service
docker compose up --build -d backend

# Access database
docker compose exec db psql -U postgres

# Access Redis
docker compose exec redis redis-cli

# View container stats
docker compose stats
```

## Next Steps

1. **Create admin user**: Use FastAPI docs to call `/auth/register`
2. **Configure OAuth**: Add Google/GitHub credentials to `.env`
3. **Add Stripe keys**: Set `STRIPE_API_KEY` and `STRIPE_WEBHOOK_SECRET`
4. **Deploy**: See [DEPLOYMENT.md](../deploy/DEPLOYMENT.md)

## Support

- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **API Schema**: http://localhost:8000/openapi.json
- **Repository**: Check GitHub Issues

---

**🎉 Your app is ready!** Start building.
