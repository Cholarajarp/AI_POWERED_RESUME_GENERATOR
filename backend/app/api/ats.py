from fastapi import APIRouter
from ..ai.ai_client import ai_client

router = APIRouter()

@router.post("/score")
async def score(payload: dict):
    # expected payload: {"resume": "...", "job": "..."}
    resume = payload.get("resume", "")
    job = payload.get("job", "")
    result = await ai_client.ats_score(resume, job)
    return result
