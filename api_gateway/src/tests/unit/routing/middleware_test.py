from httpx import AsyncClient

URL = "/healthcheck"


async def test_security_headers(async_client: AsyncClient):
    response = await async_client.get(URL)
    assert response.status_code == 200
    assert response.headers["Strict-Transport-Security"] == "max-age=31536000"
    assert response.headers["X-Content-Type-Options"] == "nosniff"


async def test_cors_regular_request(async_client: AsyncClient):
    response = await async_client.get(URL, headers={"Origin": "https://example.com"})
    assert response.status_code == 200
    assert response.headers["Access-Control-Allow-Origin"] == "*"
    assert response.headers["Access-Control-Allow-Credentials"] == "true"


async def test_cors_preflight_option_request(async_client: AsyncClient):
    headers = {
        "Origin": "https://example.com",
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "Content-Type",
    }
    response = await async_client.options(URL, headers=headers)
    all_methods = "DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT"
    assert response.status_code == 200
    assert response.headers["Access-Control-Allow-Methods"] == all_methods
    assert response.headers["Access-Control-Allow-Origin"] == "https://example.com"
    assert response.headers["Access-Control-Allow-Headers"] == "Content-Type"
    assert response.headers["Access-Control-Max-Age"] == "600"
