Title: Add Alembic env and initial migrations

Description:
There is an `alembic.ini` but no `alembic/` env or migrations. Add:

- `alembic/env.py` configured for `DATABASE_URL` and SQLAlchemy async engine.
- An initial migration to create `users` and `resumes` tables.
- Update CI to run migrations before tests if using Postgres in CI (optional).

Files to add/update:
- `backend/alembic/` directory with `env.py` and `versions/` initial migration.

Priority: High
