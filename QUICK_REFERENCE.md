# ⚡ Quick Reference Guide

## 🚀 Start Locally (Copy-Paste Ready)

```bash
# 1. Clone and setup (if not already done)
cd AI_POWERED_RESUME_GENERATOR
cp .env.example .env

# 2. Start all services
docker-compose up --build -d

# 3. Wait and verify
sleep 10
curl http://localhost:8000/health

# 4. Access the app
# Frontend:  http://localhost:3000
# API Docs:  http://localhost:8000/docs
# MinIO:     http://localhost:9001
```

---

## 📋 Production Fixes Applied

| Fix | Location | Impact |
|-----|----------|--------|
| **Config Validation** | `backend/app/core/config.py` | Fail fast on missing env vars |
| **Auto Migrations** | `backend/scripts/start.sh` | DB schema auto-created |
| **MinIO Bucket** | `backend/app/core/minio_utils.py` | File uploads work immediately |
| **Healthchecks** | `docker-compose.yml` | Service ordering automatic |
| **CORS** | `backend/app/main.py` + `frontend/vite.config.ts` | Dev & prod work without errors |
| **Health Endpoints** | `backend/app/api/health.py` | Monitor app readiness |
| **Stripe Fallback** | `backend/app/api/payments.py` | Works in dev without API key |
| **Deployment Guides** | `docs/DEPLOYMENT.md` | Deploy to Render/Vercel in 30 mins |

---

## 🧪 Test Commands

```bash
# Health checks
curl http://localhost:8000/health
curl http://localhost:8000/health/ready
curl http://localhost:8000/health/detailed

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Check environment
docker-compose exec backend env | grep OPENAI

# Run in backend container
docker-compose exec backend bash

# Stop all services
docker-compose down

# Clean rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 📚 Key Documentation

| Document | Purpose | Location |
|----------|---------|----------|
| **README.md** | Project overview + tech challenges | Root |
| **QUICKSTART.md** | 3-step local setup | `docs/` |
| **DEPLOYMENT.md** | Deploy to Render/Vercel/AWS | `docs/` |
| **PRODUCTION_READY.md** | Detailed fix documentation | `docs/` |
| **IMPLEMENTATION_SUMMARY.md** | Complete summary of all changes | Root |

---

## 🔧 Environment Variables

**Required (copy from .env.example):**
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/resume_agent_db
```

**Optional but recommended:**
```env
OPENAI_API_KEY=sk-...           # For AI features
STRIPE_API_KEY=sk_live_...      # For payments
GOOGLE_OAUTH_CLIENT_ID=...      # For Google login
GITHUB_CLIENT_ID=...            # For GitHub login
```

---

## 🐳 Docker Compose Reference

```bash
# Start services
docker-compose up -d

# Build and start
docker-compose up --build -d

# View status
docker-compose ps

# View logs
docker-compose logs -f
docker-compose logs -f backend

# Execute command
docker-compose exec backend pytest

# Stop services
docker-compose down

# Remove everything (including volumes)
docker-compose down -v
```

---

## 📱 API Endpoints

**Health Checks:**
- `GET /health` - Is app alive?
- `GET /health/ready` - Can handle requests?
- `GET /health/detailed` - Full status?

**Documentation:**
- `GET /docs` - Swagger UI (interactive)
- `GET /redoc` - ReDoc UI (documentation)

**Auth:**
- `POST /auth/login` - Local login
- `GET /auth/google` - Google OAuth
- `GET /auth/github` - GitHub OAuth

**Resume:**
- `POST /resume/upload` - Upload resume
- `GET /resume/{id}` - Get resume
- `POST /resume/{id}/analyze` - AI analysis

**Payments:**
- `POST /payments/create-checkout-session` - Create Stripe session
- `GET /payments/retrieve-session` - Get session details
- `POST /payments/manage-subscription` - Cancel/upgrade subscription

---

## 🚢 Deployment Quick Links

**Render (Backend):**
1. Create PostgreSQL database
2. Create web service pointing to backend/
3. Set environment variables
4. Deploy
- Full guide: `docs/DEPLOYMENT.md#render`

**Vercel (Frontend):**
1. Connect GitHub repo
2. Select frontend/ folder
3. Set VITE_API_URL environment variable
4. Deploy
- Full guide: `docs/DEPLOYMENT.md#vercel`

---

## 🐛 Troubleshooting

**Backend won't start:**
```bash
# Check logs
docker-compose logs backend

# Verify env file
cat .env | grep DATABASE_URL

# Check if ports are available
lsof -i :8000
```

**CORS errors:**
```bash
# Check CORS is configured
curl -i http://localhost:8000/health
# Should see Access-Control-Allow-Origin header
```

**Database errors:**
```bash
# Check database is running
docker-compose ps | grep db

# View database logs
docker-compose logs db

# Run migrations manually
docker-compose exec backend alembic upgrade head
```

**MinIO issues:**
```bash
# Check MinIO is running
docker-compose ps | grep minio

# Access MinIO console
# http://localhost:9001
# Login: miniouser / miniosecret

# Check bucket exists
docker-compose exec backend python -c \
  "from app.core.minio_utils import get_minio_client; \
   client = get_minio_client(); \
   print(client.bucket_exists('resumes'))"
```

---

## 💡 Pro Tips

1. **Use verification script:**
   ```bash
   bash scripts/verify-production-ready.sh
   ```
   Automatically checks everything

2. **Follow logs during startup:**
   ```bash
   docker-compose up --build -d && docker-compose logs -f backend
   ```
   Watch startup progress in real-time

3. **Keep .env separate:**
   ```bash
   # Never commit .env!
   echo ".env" >> .gitignore
   ```

4. **Use environment-specific configs:**
   ```bash
   # Copy and modify for production
   cp .env.example .env.production
   # Update values, then use:
   # docker-compose --env-file .env.production up -d
   ```

5. **Test health endpoints regularly:**
   ```bash
   curl http://localhost:8000/health/ready
   # Returns: {"status": "ready", "database": true, "minio": true}
   ```

---

## 📞 Quick Support

**Can't start services?**
→ Run verification script: `bash scripts/verify-production-ready.sh`

**Missing environment variables?**
→ Copy template: `cp .env.example .env`

**Want to deploy?**
→ Follow: `docs/DEPLOYMENT.md`

**Need detailed explanation?**
→ Read: `IMPLEMENTATION_SUMMARY.md`

**API documentation?**
→ Visit: `http://localhost:8000/docs`

---

## ✅ Verification Checklist

```bash
# Prerequisites (should pass)
docker --version
docker-compose --version
curl --version

# Environment (should have .env with DATABASE_URL)
ls -la .env
grep DATABASE_URL .env

# Services (should all show "Up")
docker-compose up --build -d
sleep 10
docker-compose ps

# Health (should all return 200)
curl -w "%{http_code}\n" http://localhost:8000/health
curl -w "%{http_code}\n" http://localhost:8000/health/ready
curl -w "%{http_code}\n" http://localhost:8000/health/detailed

# Access (should load)
curl http://localhost:3000         # Frontend
curl http://localhost:8000/docs    # API docs
```

All green ✅? You're ready to deploy!

---

**Last Updated:** November 17, 2025
**Version:** 1.0.0
**Status:** Production-Ready ✅
