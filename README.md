# AI Interview & Resume Agent

A production-ready SaaS platform to help users optimize resumes for ATS, analyze job descriptions, and practice AI-scored mock interviews with voice feedback.

**Tech Stack**
- Frontend: React 18 + Vite + TypeScript + Tailwind CSS
- Backend: FastAPI (Python 3.11+) + SQLAlchemy async + Pydantic
- Database: PostgreSQL
- Cache/Queue: Redis + Celery
- Storage: MinIO (S3-compatible)
- Auth: JWT + OAuth2 (Google)
- Payments: Stripe
- CI/CD: GitHub Actions
- Deployment: Docker + docker-compose

---

## Quick Start (Development)

### Prerequisites
- **Docker Desktop** (Windows/Mac) or Docker Engine (Linux) with Docker Compose V2
  - Download: https://www.docker.com/get-started
- **Git**

### Start the Full Stack

1. Clone and navigate to the repo:
```powershell
cd C:\Users\YourUser\Downloads\AI_POWERED_RESUME_GENERATOR
```

2. Run the automated start script (PowerShell):
```powershell
.\scripts\start-dev.ps1
```

   Or manually:
```powershell
# Create .env if missing
Copy-Item .env.example .env

# Start services (Docker Compose V2)
docker compose up --build -d

# Or if using legacy docker-compose
docker-compose up --build -d

# Create admin user
docker compose exec backend python scripts/create_admin.py --email admin@example.com --password secret
```

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