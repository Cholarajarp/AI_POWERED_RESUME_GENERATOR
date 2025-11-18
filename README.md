# AI Interview & Resume Agent

A production-ready SaaS platform to help users optimize resumes for ATS, analyze job descriptions, and practice AI-scored mock interviews with voice feedback.

**Tech Stack**
- Frontend: React 18 + Vite + TypeScript + Tailwind CSS
- Backend: FastAPI (Python 3.11+) + SQLAlchemy async + Pydantic
- Database: PostgreSQL
- Cache/Queue: Redis + Celery
- Storage: MinIO (S3-compatible)
- Auth: JWT + OAuth2 (Google/GitHub) 
- Payments: Stripe
- CI/CD: GitHub Actions
- Deployment: Docker + docker-compose

---

## Key Features

### Core Features
- **Resume Optimization**: AI-powered ATS keyword matching & formatting
- **Job Analysis**: Parse job descriptions and match with resume
- **Mock Interviews**: AI interviewer with voice feedback
- **Template System**: Cover letters, LinkedIn profiles, ATS templates
- **PDF Export**: Premium resume templates with custom styling

### Advanced Features
- **OAuth Login**: Google & GitHub authentication
- **Subscription Plans**: Stripe billing with 3 tiers (Basic/Pro/Enterprise)
- **Admin Dashboard**: Real-time analytics & user management
- **Celery Tasks**: Async resume processing and email notifications

---

## Quick Start (Development)

### Prerequisites
- **Docker Desktop** (Windows/Mac) or Docker Engine (Linux) with Docker Compose
  - Download: https://www.docker.com/get-started
- **Git**

### Start in 3 Steps

1. **Clone and create .env**:
```bash
cd AI_POWERED_RESUME_GENERATOR
cp .env.example .env
# Edit .env with your secrets (OPENAI_API_KEY, STRIPE_API_KEY, etc.)
```

2. **Start all services**:
```bash
docker compose up --build -d
```

3. **Access the app**:
- Frontend: http://localhost:3000
- API: http://localhost:8000/docs
- MinIO: http://localhost:9001

**Full guide**: See [QUICKSTART.md](docs/QUICKSTART.md)

---

##  Project Structure

```
AI_POWERED_RESUME_GENERATOR/
├── backend/
│   ├── app/
│   │   ├── api/              # Route handlers (auth, resume, payments, etc.)
│   │   ├── core/             # Config, security, logging
│   │   ├── db/               # Database models & CRUD
│   │   ├── ai/               # OpenAI & LLM integrations
│   │   ├── utils/            # Helper functions
│   │   └── main.py           # FastAPI app entry point
│   ├── alembic/              # Database migrations
│   ├── scripts/              # Admin scripts, startup
│   ├── Dockerfile            # Backend container
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── pages/            # React pages (Login, Dashboard, etc.)
│   │   ├── components/       # Reusable components
│   │   ├── services/         # API client & utilities
│   │   └── App.tsx           # Main React app
│   ├── Dockerfile            # Frontend container
│   └── package.json          # NPM dependencies
├── deploy/
│   └── DEPLOYMENT.md         # Render/Vercel/AWS guides
├── docs/
│   ├── QUICKSTART.md         # 3-step setup guide
│   └── API.md                # API documentation
├── scripts/
│   ├── start-dev.ps1         # Windows startup script
│   └── health-check.sh       # System diagnostics
└── docker-compose.yml        # Multi-service orchestration
```

---

## Technical Challenges Solved

This section highlights the engineering decisions and solutions implemented to build a production-grade SaaS platform.

### 1. **Async SQLAlchemy + Alembic Database Management**
**Challenge:** Traditional SQLAlchemy is synchronous; FastAPI is async-first. Mixing them causes blocking.

**Solution:**
- SQLAlchemy 2.0 async mode with `asyncpg` driver for non-blocking database calls
- Async context managers for session management
- Alembic auto-migrations running on container startup (prevents "table not found" errors)
- Proper connection pooling for concurrent requests

**Code Example:**
```python
# async/await throughout
async def get_user(user_id: int):
    async with AsyncSession() as session:
        user = await session.get(User, user_id)
        return user
```

---

### 2. **MinIO S3-Compatible Storage**
**Challenge:** AWS S3 is expensive; local file storage doesn't scale; need S3 API compatibility for easy cloud migration.

**Solution:**
- MinIO server deployed alongside backend with Docker Compose
- Bucket auto-creation on app startup (prevents "bucket not found" errors)
- Async file upload/download with pre-signed URLs
- Drop-in replacement for S3 (same API, easy migration)

**Code Example:**
```python
# MinIO auto-initialization
@app.on_event("startup")
async def startup():
    ensure_buckets()  # Create if missing
```

---

### 3. **OAuth2 + JWT Multi-Provider Authentication**
**Challenge:** Multiple OAuth providers (Google, GitHub) with secure token management and auto-refresh.

**Solution:**
- Separate OAuth flow for each provider with proper PKCE
- JWT tokens with automatic refresh mechanism
- Secure storage of refresh tokens in httponly cookies
- Provider-agnostic authentication layer

**Supported Providers:**
- Google OAuth (email + profile)
- GitHub OAuth (username + profile picture)
- Future: LinkedIn, Microsoft

---

### 4. **Real-time OpenAI Integration with Streaming**
**Challenge:** API calls to OpenAI can be slow; need real-time feedback for interview simulations.

**Solution:**
- Streaming responses using FastAPI `StreamingResponse`
- Prompt engineering for resume analysis (context-aware templates)
- Token usage tracking for cost monitoring
- Rate-limiting and error recovery

**Features:**
- Resume optimization suggestions (real-time feedback)
- Mock interview questions (AI-generated dynamically)
- Interview feedback (voice + text)
- Rate-limit handling with exponential backoff

---

### 5. **Stripe Subscription Billing**
**Challenge:** Complex payment flows with different plan tiers, upgrades, cancellations, and webhook security.

**Solution:**
- Full Stripe integration with Checkout Sessions
- Subscription tier management (Basic/Pro/Enterprise)
- Upgrade/downgrade/cancel flows with proration
- Webhook signature verification for security
- Dev-mode graceful degradation (payments optional in dev)

**Supported Operations:**
- One-time checkout
- Subscription creation with retry logic
- Plan upgrades/downgrades with automatic billing adjustment
- Cancellation with grace period
- Webhook handling for payment events

---

### 6. **Docker Multi-Service Orchestration**
**Challenge:** 6 services (PostgreSQL, Redis, MinIO, Backend, Celery, Frontend) with dependencies, migrations, and health monitoring.

**Solution:**
- Docker Compose v3.8+ with service health checks
- Proper startup ordering using `depends_on: condition: service_healthy`
- Auto-migration script that waits for DB readiness
- Named volumes for persistent data
- Custom bridge network for service isolation

**Services Managed:**
- PostgreSQL (database)
- Redis (cache + Celery broker)
- MinIO (S3-compatible storage)
- FastAPI backend (uvicorn)
- Celery worker (async tasks)
- React frontend (Vite dev server)

**Smart Startup:**
1. Database waits for pg_isready
2. Redis pings itself
3. MinIO checks health endpoint
4. Backend waits for all 3, runs migrations, creates bucket
5. Celery waits for backend ready
6. Frontend can access all APIs

---

### 7. **Configuration Management with Pydantic**
**Challenge:** Environment variables without validation cause cryptic runtime errors in production.

**Solution:**
- Pydantic BaseSettings with required field validation
- Custom validators for DATABASE_URL, MINIO_ENDPOINT
- Helpful error messages listing all required variables
- Dev/prod environment detection

**Error Output (Missing Env Var):**
```
===== CONFIGURATION ERROR =====
DATABASE_URL is required
REQUIRED variables (must be set in .env):
  • DATABASE_URL       - PostgreSQL connection string
  • MINIO_ENDPOINT     - MinIO server address
...
Quick fix:
  1. Copy .env.example to .env
  2. Fill in required values
  3. Restart the application
```

---

### 8. **CORS + Vite Proxy Development**
**Challenge:** Frontend on port 3000, backend on 8000 = CORS errors in dev and prod.

**Solution:**
- Vite proxy for dev mode (`/api` → `http://localhost:8000`)
- CORS middleware for production (environment-aware origin handling)
- Axios interceptor for token attachment
- Automatic frontend URL detection from environment

**Development:**
```typescript
// vite.config.ts
proxy: {
  '/api': 'http://localhost:8000'
}
```

**Production:**
```python
# Restrict to frontend domain only
cors_origins = [settings.FRONTEND_URL]
```

---

### 9. **Health Checks & Readiness Probes**
**Challenge:** Containers start but services aren't ready; backend crashes trying to reach database.

**Solution:**
- `/health` endpoint for liveness probes
- `/health/ready` endpoint with database + MinIO checks
- `/health/detailed` for debugging
- Kubernetes-compatible health check format

**Endpoints:**
- `GET /health` - Simple "is alive" check
- `GET /health/ready` - Can handle requests? (DB + MinIO)
- `GET /health/detailed` - Full service status report

---

### 10. **Celery + Redis Async Task Queue**
**Challenge:** Long-running operations (resume analysis, email) block request handlers.

**Solution:**
- Celery worker pool with Redis broker
- Async task decoration for resume analysis
- Task result caching in Redis
- Retry logic with exponential backoff

**Tasks Managed:**
- Resume PDF generation (async)
- Email notifications (async)
- OpenAI batch requests
- Stripe webhook processing

---

## Documentation

- **[QUICKSTARTg .md](docs/QUICKSTART.md)** - Get running in 3 steps
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Deploy to Render, Vercel, AWS
- **[API Docs](http://localhost:8000/docs)** - Swagger interactive API
- **[Architecture](docs/ARCHITECTURE.md)** - System design details

---

## Environment Variables

Required (copy from `.env.example`):
```env
DATABASE_URL=postgresql+asyncpg://...
OPENAI_API_KEY=sk-...
STRIPE_API_KEY=sk_live_...
MINIO_ROOT_USER=miniouser
MINIO_ROOT_PASSWORD=miniosecret
```

Optional:
```env
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
GOOGLE_OAUTH_CLIENT_ID=...
GOOGLE_OAUTH_CLIENT_SECRET=...
```

---

## Testing & Validation

```bash
# Run backend tests
docker compose exec backend pytest

# Run frontend tests
docker compose exec frontend npm test

# Health check
./scripts/health-check.sh

# View logs
docker compose logs -f backend
docker compose logs -f frontend
```

---

## Deployment

### Quick Deploy Links
- **Render** (Backend): See [DEPLOYMENT.md](docs/DEPLOYMENT.md#render-backend--database)
- **Vercel** (Frontend): See [DEPLOYMENT.md](docs/DEPLOYMENT.md#vercel-frontend)
- **AWS** (Full Stack): See [DEPLOYMENT.md](docs/DEPLOYMENT.md#aws-alternative)

### Production Checklist
- [ ] Set strong `SECRET_KEY` in production
- [ ] Update `FRONTEND_URL` to production domain
- [ ] Configure OAuth client IDs/secrets
- [ ] Set Stripe production keys
- [ ] Enable HTTPS/SSL everywhere
- [ ] Set up database backups
- [ ] Configure email notifications
- [ ] Enable monitoring & logging (Sentry)

---

## Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Commit changes: `git commit -m "feat: add feature"`
3. Push and create a Pull Request

---

## License

MIT License - See [LICENSE](LICENSE) file

---

## Support & Contact

- Email: contact@airesume.dev
- Issues: [GitHub Issues](https://github.com/yourusername/ai-resume-agent/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/ai-resume-agent/discussions)

---

**Built with for job seekers everywhere.**

3. Access services:
- **Backend API**: http://localhost:8000
- **OpenAPI Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000
- **MinIO Console**: http://localhost:9000 (user: `miniouser`, pass: `miniosecret`)

### Stop Services
```powershell
docker compose down -v   # -v removes volumes (clean slate)
docker compose down      # keeps volumes
```

### View Logs
```powershell
docker compose logs -f backend     # Follow backend logs
docker compose logs -f frontend    # Follow frontend logs
docker compose logs --tail 50 db   # Last 50 lines of DB
```

---

## Development Workflow

### Backend Development (with hot-reload)
The backend container uses `--reload` in uvicorn, so code changes auto-reload:
```powershell
# Edit backend code and save; changes hot-reload
docker compose logs -f backend

# Run tests inside container
docker compose exec backend pytest -q
```

### Frontend Development
The frontend runs in dev mode with Vite hot-reload:
```powershell
# Edit React components and save; changes hot-reload in browser
docker compose logs -f frontend

# Access at http://localhost:3000
```

### Environment Variables
Edit `.env` to customize:
- `OPENAI_API_KEY` — for AI features (required for full functionality)
- `STRIPE_API_KEY` — for payment integration
- `DATABASE_URL` — already set to Postgres in docker-compose
- See `.env.example` for all options

---

## Testing

### Run Backend Tests
```powershell
docker compose exec backend pytest -q
```

### Run Frontend Tests
```powershell
docker compose exec frontend npm test
```

### CI/CD
GitHub Actions runs tests on every push and PR:
- `.github/workflows/ci-tests.yml` — runs pytest + frontend tests
- `.github/workflows/deploy.yml` — builds Docker images

See workflow logs in GitHub Actions tab.

---

## Key Files & Directories

```
.
├── backend/               # FastAPI application
│   ├── app/
│   │   ├── api/          # Route handlers (auth, resume, interview, etc.)
│   │   ├── db/           # SQLAlchemy models, CRUD ops
│   │   ├── ai/           # AI client + prompt templates
│   │   ├── core/         # Config, security, logging, rate limiting
│   │   ├── tests/        # pytest tests
│   │   └── main.py       # FastAPI app entry
│   ├── scripts/
│   │   └── create_admin.py  # Admin user seed script
│   ├── requirements.txt
│   ├── Dockerfile
│   └── alembic.ini
├── frontend/              # React + Vite app
│   ├── src/
│   │   ├── pages/        # Landing, Dashboard, MockInterview
│   │   ├── App.tsx       # Router
│   │   └── main.tsx      # Entry
│   ├── package.json
│   ├── Dockerfile
│   └── vite.config.ts
├── docker-compose.yml     # Orchestration: backend, frontend, db, redis, minio, celery
├── .github/workflows/     # GitHub Actions CI/CD
├── docs/                  # API spec, marketing copy, issues
└── README.md (this file)
```

---

## Architecture Overview

### Services (docker-compose)
1. **db** (PostgreSQL) — stores users, resumes, sessions, payments
2. **redis** — caching & Celery broker
3. **minio** — S3-compatible storage for resume files
4. **backend** — FastAPI server (port 8000)
5. **frontend** — React dev server (port 3000)
6. **celery** — task queue worker for long-running jobs

### Key Endpoints
- `POST /auth/register`, `/auth/login` — user auth
- `POST /resume/upload` — upload resume (stores to MinIO)
- `POST /job/parse` — extract keywords from job description
- `POST /ats/score` — AI-powered ATS scoring
- `POST /interview/session/create` — start mock interview
- `POST /interview/session/{id}/submit_answer` — evaluate answer
- `POST /payments/create-checkout-session` — Stripe checkout
- Admin endpoints under `/admin/*`

See `docs/api.md` for full API specification.

---

## Known Issues & TODOs

See `docs/ISSUES_TO_FIX.md` for a list of high-priority items:
- Implement refresh token flow
- MinIO persistence for uploads (partial)
- Stripe webhook signature verification (TODO)
- Alembic migrations setup
- Whisper speech-to-text integration

Contributions welcome!

---

## Troubleshooting

**Docker not found?**
- Install Docker Desktop: https://www.docker.com/get-started
- Ensure Docker daemon is running (start Docker Desktop)

**Container fails to start?**
```powershell
docker compose logs db        # check database logs
docker compose logs backend   # check app logs
docker compose down -v        # reset volumes and retry
```

**Backend can't connect to DB?**
- Ensure `DATABASE_URL` in `.env` is `postgresql+asyncpg://postgres:postgres@db:5432/resume_agent_db`
- Wait 5-10 seconds for Postgres to be ready (`docker compose logs db`)

**Port already in use?**
- Change port in `docker-compose.yml` (e.g., `8001:8000` for backend)
- Or kill the process: `netstat -ano | findstr :8000` (Windows)

---

## Next Steps

1. **Review .env** — add real secrets (OpenAI key, Stripe key, etc.)
2. **Create admin user** — already done by start script
3. **Test endpoints** — visit http://localhost:8000/docs and try the API
4. **Deploy** — see `deploy/README.md` for cloud deployment options

---

## License
MIT