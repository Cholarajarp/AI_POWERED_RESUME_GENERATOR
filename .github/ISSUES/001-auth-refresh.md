Title: Implement refresh token flow for JWT auth

Description:
The `/auth/refresh` endpoint currently returns 501 Not Implemented. Implement a secure refresh token flow:

- Store refresh tokens in DB (rotate on use).
- Issue access tokens (short-lived) and refresh tokens (longer-lived, revocable).
- Provide endpoint `/auth/refresh` that accepts a refresh token and returns new access token (and a new refresh token).
- Add tests for refresh token rotation and revocation.

Files to update:
- `backend/app/api/auth.py`
- Add DB model for refresh tokens (`backend/app/db/models.py`)
- `backend/app/db/crud.py`

Priority: High
