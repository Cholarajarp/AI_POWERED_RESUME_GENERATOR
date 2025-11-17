import pytest
from httpx import AsyncClient
from ..main import app

@pytest.mark.asyncio
async def test_ready_and_register():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get('/health/ready')
        assert r.status_code == 200
        # register flow (uses in-memory DB placeholder) - expecting 200 or 400
        payload = {"email": "alice@example.com", "password": "secret"}
        r2 = await ac.post('/auth/register', json=payload)
        assert r2.status_code in (200, 400)
