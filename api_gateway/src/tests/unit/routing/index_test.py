import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("url", ["/", "/docs"])
async def test_security_headers(async_client: AsyncClient, url: str):
    response = await async_client.get(url)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
