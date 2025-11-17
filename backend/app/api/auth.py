from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from ..core.config import settings
from ..core.security import create_access_token, verify_password, get_password_hash
from ..db import crud

router = APIRouter()

class RegisterIn(BaseModel):
    email: str
    password: str
    full_name: str | None = None

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=TokenOut)
async def register(data: RegisterIn):
    user = await crud.get_user_by_email(data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new = await crud.create_user(email=data.email, password=data.password, full_name=data.full_name)
    access = create_access_token({"sub": new.email})
    return {"access_token": access}

class LoginIn(BaseModel):
    email: str
    password: str

@router.post("/login", response_model=TokenOut)
async def login(data: LoginIn):
    user = await crud.get_user_by_email(data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access = create_access_token({"sub": user.email})
    return {"access_token": access}

@router.post("/refresh", response_model=TokenOut)
async def refresh():
    # TODO: implement refresh token flow
    raise HTTPException(status_code=501, detail="Not implemented")

@router.get("/oauth/google")
async def oauth_google():
    # TODO: implement OAuth2 flow
    return {"msg": "google oauth placeholder"}
