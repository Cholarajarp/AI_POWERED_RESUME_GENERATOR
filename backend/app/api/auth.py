from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import httpx
import jwt
from datetime import datetime, timedelta
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

class GoogleTokenRequest(BaseModel):
    token: str

@router.post("/google/callback", response_model=TokenOut)
async def google_callback(request: GoogleTokenRequest):
    """Handle Google OAuth callback"""
    try:
        # Verify token with Google
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://www.googleapis.com/oauth2/v1/userinfo",
                headers={"Authorization": f"Bearer {request.token}"}
            )
        
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid Google token")
        
        user_data = response.json()
        email = user_data.get("email")
        name = user_data.get("name")
        
        # Get or create user
        user = await crud.get_user_by_email(email)
        if not user:
            user = await crud.create_user(
                email=email,
                password="oauth_user",
                full_name=name,
                oauth_provider="google"
            )
        
        access_token = create_access_token({"sub": user.email, "user_id": user.id})
        return {"access_token": access_token}
    
    except Exception as e:
        raise HTTPException(status_code=401, detail="Google authentication failed")

class GitHubTokenRequest(BaseModel):
    code: str

@router.post("/github/callback", response_model=TokenOut)
async def github_callback(request: GitHubTokenRequest):
    """Handle GitHub OAuth callback"""
    try:
        # Exchange code for access token
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                "https://github.com/login/oauth/access_token",
                data={
                    "client_id": settings.GITHUB_CLIENT_ID,
                    "client_secret": settings.GITHUB_CLIENT_SECRET,
                    "code": request.code
                },
                headers={"Accept": "application/json"}
            )
        
        if token_response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid GitHub code")
        
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        
        # Get user info
        async with httpx.AsyncClient() as client:
            user_response = await client.get(
                "https://api.github.com/user",
                headers={"Authorization": f"Bearer {access_token}"}
            )
        
        if user_response.status_code != 200:
            raise HTTPException(status_code=401, detail="Failed to get GitHub user info")
        
        user_data = user_response.json()
        email = user_data.get("email")
        login = user_data.get("login")
        
        # If no email, try to get it from emails endpoint
        if not email:
            async with httpx.AsyncClient() as client:
                emails_response = await client.get(
                    "https://api.github.com/user/emails",
                    headers={"Authorization": f"Bearer {access_token}"}
                )
            emails = emails_response.json()
            email = next((e["email"] for e in emails if e["primary"]), emails[0]["email"])
        
        # Get or create user
        user = await crud.get_user_by_email(email)
        if not user:
            user = await crud.create_user(
                email=email,
                password="oauth_user",
                full_name=login,
                oauth_provider="github"
            )
        
        access_token = create_access_token({"sub": user.email, "user_id": user.id})
        return {"access_token": access_token}
    
    except Exception as e:
        raise HTTPException(status_code=401, detail="GitHub authentication failed")

