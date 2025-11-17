from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
async def list_users():
    # TODO: implement admin user listing with pagination
    return {"users": []}

@router.get("/metrics")
async def metrics():
    # TODO: return usage metrics
    return {"active_users": 0, "interviews": 0}
