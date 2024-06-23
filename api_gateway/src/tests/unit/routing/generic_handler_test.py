from http import HTTPMethod, HTTPStatus
from typing import Any, NoReturn
from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient

from adapters.exceptions import GatewayRouterException, NotFoundException
from drivers.rest.dependencies.gateway_router import (
    get_gateway_router,
    get_generic_gateway_router,
)
from drivers.rest.main import app
from tests.conftest import create_jwt


@pytest.mark.parametrize(
    "path, method",
    (
        ("/test-service/items/1", HTTPMethod.GET),
        ("/test-service/items/1", HTTPMethod.PATCH),
        ("/test-service/items/1", HTTPMethod.DELETE),
        ("/test-service/items", HTTPMethod.POST),
        ("/test-service/items", HTTPMethod.GET),
        ("/another-service/user/50/", HTTPMethod.GET),
        ("/another-service/user/50/", HTTPMethod.PATCH),
        ("/another-service/user/50/", HTTPMethod.DELETE),
        ("/another-service/user/", HTTPMethod.POST),
        ("/another-service/user/", HTTPMethod.GET),
    ),
)
async def test_generic_router_is_called(
    async_client: AsyncClient, path: str, method: HTTPMethod
):
    mocked_router = AsyncMock(return_value=(b"", HTTPStatus.OK))
    app.dependency_overrides[get_generic_gateway_router] = lambda: mocked_router

    headers = {"Authorization": f"Bearer {create_jwt()}"}
    await async_client.request(method, path, headers=headers)
    mocked_router.assert_called_once()


@pytest.mark.parametrize(
    "exc, status",
    (
        (GatewayRouterException(), HTTPStatus.BAD_REQUEST),
        (NotFoundException(), HTTPStatus.NOT_FOUND),
    ),
)
async def test_generic_router_exceptions(
    async_client: AsyncClient, exc: Exception, status: HTTPStatus
):
    class MockGatewayRouter:
        async def __call__(self, *args: Any, **kwargs: Any) -> NoReturn:
            raise exc

    app.dependency_overrides[get_gateway_router] = MockGatewayRouter
    response = await async_client.get(
        "/test-service/item/1", headers={"Authorization": f"Bearer {create_jwt()}"}
    )
    assert response.status_code == status
    assert response.json() == {"detail": str(exc)}


async def test_generic_router_not_authorized(async_client: AsyncClient):
    response = await async_client.get("/test-service/item/1")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Not authorized"}
