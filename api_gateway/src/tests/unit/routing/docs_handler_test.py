from http import HTTPStatus
from typing import Any

from httpx import AsyncClient

from drivers.rest.dependencies.gateway_router import get_openapi_gateway_router
from drivers.rest.main import app

openapi_json = b'{"openapi":"3.1.0","info":{"title":"Service B","version":"0.1.0"},"paths":{"/hello":{"get":{"summary":"Hello","operationId":"hello_hello_get","responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}}}}}}}'
service = "service-a"


async def test_docs_success(async_client: AsyncClient):
    response = await async_client.get(f"/{service}/docs")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert f"/{service}/openapi.json" in response.content.decode()


async def test_static_success(async_client: AsyncClient):
    response = await async_client.get("/static/favicon.png")
    assert response.status_code == 200


async def test_openapi_router_success(async_client: AsyncClient):
    class MockGatewayRouter:
        async def __call__(self, *args: Any, **kwargs: Any) -> tuple[bytes, int]:
            return openapi_json, HTTPStatus.OK

    app.dependency_overrides[get_openapi_gateway_router] = MockGatewayRouter

    response = await async_client.get(f"/{service}/openapi.json")
    for path in response.json()["paths"]:
        assert path.startswith(f"/{service}")
