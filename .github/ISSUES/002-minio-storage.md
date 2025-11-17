Title: Implement MinIO storage and resume upload persistence

Description:
The resume `/resume/upload` endpoint currently decodes the uploaded file but does not persist it to MinIO or create a DB record. Implement:

- MinIO client integration (`boto3` or `minio`), upload files to `MINIO_BUCKET`.
- Create `Resume` DB record with `s3_key` and `user_id`.
- Implement `/resume/download` to stream from MinIO.
- Add unit tests that mock MinIO client.

Files to update:
- `backend/app/api/resume.py`
- `backend/app/db/models.py` (ensure Resume model exists)

Priority: High
