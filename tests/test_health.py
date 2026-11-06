import pytest
from httpx import AsyncClient
from backend.app.database.connection import check_database_connectivity


@pytest.mark.asyncio
async def test_health_endpoint(async_client: AsyncClient):
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "healthy"
    assert data["data"]["service"] == "Script Scrapper"
    assert "version" in data["data"]
    assert "timestamp" in data["data"]


@pytest.mark.asyncio
async def test_system_status_endpoint(async_client: AsyncClient):
    response = await async_client.get("/api/v1/system/status")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "operational"
    assert data["data"]["database"]["connected"] is True
    assert data["data"]["database"]["status"] == "online"
    
    server_info = data["data"]["server"]
    assert server_info["configured_workers"] == 2
    assert server_info["per_worker_pool_max"] == 20
    assert server_info["aggregate_api_peak_ceiling"] == 40


@pytest.mark.asyncio
async def test_database_connectivity_direct():
    result = await check_database_connectivity()
    assert result["connected"] is True
    assert result["status"] == "online"
    assert "pool" in result
    assert result["pool"]["configured_pool_size"] == 15
    assert result["pool"]["configured_max_overflow"] == 5


@pytest.mark.asyncio
async def test_not_found_standard_envelope(async_client: AsyncClient):
    response = await async_client.get("/api/v1/nonexistent-endpoint")
    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert "error" in data
    assert data["error"]["code"] == "RESOURCE_NOT_FOUND"
