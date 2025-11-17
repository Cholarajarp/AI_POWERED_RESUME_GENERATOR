from sqlalchemy.future import select
from sqlalchemy import insert
from .models import User
from .database import AsyncSessionLocal
from ..core.security import get_password_hash

async def get_user_by_email(email: str):
    async with AsyncSessionLocal() as session:
        q = await session.execute(select(User).where(User.email == email))
        return q.scalars().first()

async def create_user(email: str, password: str, full_name: str | None = None):
    hashed = get_password_hash(password)
    async with AsyncSessionLocal() as session:
        user = User(email=email, hashed_password=hashed, full_name=full_name)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
