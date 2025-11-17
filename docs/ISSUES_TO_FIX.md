# Issues & Suggested Fixes

This file lists problems found in the repository and suggested remediation steps. Create GitHub issues from these items and address them in focused PRs.

1. Auth: Refresh token flow unimplemented
   - File: `backend/app/api/auth.py`
   - Description: `/auth/refresh` raises 501 Not Implemented. Implement refresh tokens (store refresh tokens in DB, rotate, revoke).
   - Priority: High

2. Auth: OAuth2 Google not implemented
   - File: `backend/app/api/auth.py`
   - Description: `/auth/oauth/google` is a placeholder. Implement OAuth2 Authorization Code flow and connect to user records.
   - Priority: Medium

3. Storage: MinIO integration missing
   - Files: `backend/app/api/resume.py`, `backend/app/db/models.py`
   - Description: Upload handler decodes file but does not store to MinIO or create Resume DB record. Implement MinIO client (boto3 or minio) and save S3 keys.
   - Priority: High

4. Transcription: Whisper integration missing
   - File: `backend/app/api/interview.py`
   - Description: `/interview/transcribe` is a stub. Add a pluggable interface to call OpenAI Whisper or a local fallback and return structured transcript.
   - Priority: Medium

5. Rate limiting: Redis-backed middleware not implemented
   - File: `backend/app/core/rate_limiter.py`
   - Description: SimpleRateLimiter is a placeholder. Implement Redis/aioredis token-bucket or fixed-window limiter and add tests.
   - Priority: Medium

6. Payments: Stripe webhook verification
   - File: `backend/app/api/payments.py`
   - Description: Webhook handler doesn't verify signature nor handle events. Use `stripe.Webhook.construct_event` and implement event handling (invoice.payment_succeeded, checkout.session.completed).
   - Priority: High

7. DB: Alembic migrations and models incomplete
   - Files: `backend/alembic.ini`, `backend/alembic/` (missing)
   - Description: Add alembic env and initial migration to create users/resumes tables.
   - Priority: High

8. Tests: Some tests depend on DB/migrations
   - Files: `backend/app/tests/*`
   - Description: Tests assume DB exists; either use SQLite in-memory for unit tests or a test Postgres service in CI and run migrations beforehand.
   - Priority: Medium

9. Frontend: missing build artifacts and tests
   - Files: `frontend/` - CI attempts to run `npm test` but project has no tests configured. Add sample Vitest tests or update CI.
   - Priority: Low

10. CI: deploy workflow incomplete
    - File: `.github/workflows/deploy.yml`
    - Description: The workflow builds images but does not push to a registry. Add registry login and push steps and optional image tags.
    - Priority: Low

11. Docs: README references admin seed script but script missing
    - Files: `README.md` and `backend/scripts/create_admin.py` (missing)
    - Description: Add script to create an admin user using the DB models and environment variables.
    - Priority: Low

12. Misc: Many TODO placeholders in code
    - Action: Search for `TODO` and `placeholder` and create small issues or tasks for each. This file was generated from the repo scan.


---
How to use

- Create issues in GitHub for the high-priority items first (Auth refresh, Storage, Webhooks, Migrations).
- Work in small PRs and add tests for each change.
