"""Simple admin creation script for local dev.

Usage:
    python create_admin.py --email admin@example.com --password secret

This script connects using the DATABASE_URL from env and creates an admin user.
"""
import os
import argparse
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.models import User, Base

async def main(email: str, password: str):
    engine = create_async_engine(settings.DATABASE_URL)
    AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        hashed = get_password_hash(password)
        user = User(email=email, hashed_password=hashed, full_name='Admin', is_admin=True)
        session.add(user)
        await session.commit()
        print(f"Created admin user: {email}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--email', required=True)
    parser.add_argument('--password', required=True)
    args = parser.parse_args()
    asyncio.run(main(args.email, args.password))
