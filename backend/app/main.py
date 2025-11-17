from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api import auth, health, user, resume, job, ats, interview, payments, admin
from .core.logging import setup_logging

setup_logging()

app = FastAPI(title="AI Interview & Resume Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"]) 
app.include_router(resume.router, prefix="/resume", tags=["resume"])
app.include_router(job.router, prefix="/job", tags=["job"])
app.include_router(ats.router, prefix="/ats", tags=["ats"])
app.include_router(interview.router, prefix="/interview", tags=["interview"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

@app.on_event("startup")
async def startup():
    # TODO: connect to DB, init pools
    pass
