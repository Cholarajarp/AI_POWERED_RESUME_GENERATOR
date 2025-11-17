import pytest
from httpx import AsyncClient
from ..main import app

@pytest.mark.asyncio
async def test_ready():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/health/ready")
        assert r.status_code == 200
        assert r.json().get("status") == "ok"
