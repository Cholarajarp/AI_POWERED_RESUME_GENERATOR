from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/ready")
async def ready():
    return JSONResponse({"status": "ok"})

@router.get("/live")
async def live():
    return JSONResponse({"status": "alive"})
