# AI Interview & Resume Agent

Local development scaffold for AI Interview & Resume Agent — a SaaS to optimize resumes, run ATS analysis, and practice AI-scored mock interviews.

Quick start (development):

1. Copy env vars:

```powershell
cp .env.example .env
# then edit .env to add keys
```

2. Build and run with Docker Compose:

```powershell
docker-compose up --build
```

3. Backend API will be at `http://localhost:8000` and frontend at `http://localhost:3000`.

Useful commands:
- `docker-compose up --build` — start services
- `docker-compose down -v` — stop and remove volumes
- `backend` container: run migrations with `alembic` and create admin seed script

See `docs/` for API specification and other docs.
