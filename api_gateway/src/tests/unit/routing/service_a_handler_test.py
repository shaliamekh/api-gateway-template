from http import HTTPMethod, HTTPStatus
from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient

from drivers.rest.dependencies.gateway_router import get_auth_gateway_router
from drivers.rest.main import app


@pytest.mark.parametrize(
    "path, method",
    (
        ("/service-a/auth/login", HTTPMethod.POST),
        ("/service-a/auth/signup", HTTPMethod.POST),
        ("/service-a/auth/refresh", HTTPMethod.POST),
    ),
)
async def test_auth_router_is_called(
    async_client: AsyncClient, path: str, method: HTTPMethod
):
    mocked_router = AsyncMock(return_value=(b"", HTTPStatus.OK))
    app.dependency_overrides[get_auth_gateway_router] = lambda: mocked_router

    await async_client.request(method, path)
    mocked_router.assert_called_once()
