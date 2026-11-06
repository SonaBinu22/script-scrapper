import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from backend.app.main import app


@pytest_asyncio.fixture
async def async_client():
    async with ASGITransport(app=app) as transport:
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
