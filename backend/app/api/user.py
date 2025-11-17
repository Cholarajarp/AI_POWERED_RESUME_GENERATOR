from fastapi import APIRouter, Depends, HTTPException
from ..db import crud

router = APIRouter()

@router.get("/me")
async def me():
    # TODO: return current user from token
    return {"msg": "user me placeholder"}

@router.get("/subscription")
async def subscription():
    # TODO: return subscription status
    return {"subscription": "free", "credits": 10}
