# API Overview

FastAPI application exposes several endpoints:

- `POST /auth/register` — register
- `POST /auth/login` — login get access token
- `POST /auth/refresh` — token refresh (TODO)
- `GET /user/me` — user profile
- `POST /resume/upload` — upload resume file
- `POST /job/parse` — extract keywords from job description
- `POST /ats/score` — ATS scoring (uses AI)
- `POST /interview/*` — interview session endpoints
- `POST /payments/create-checkout-session` — Stripe flow
- `POST /payments/webhook` — webhook

OpenAPI docs available at `/docs` when server is running.
