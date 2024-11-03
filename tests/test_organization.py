import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_get_organization():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/organizations/11")
    assert response.status_code == 200
    assert "id" in response.json()