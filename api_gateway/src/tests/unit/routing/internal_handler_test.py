from http import HTTPMethod, HTTPStatus

import pytest
from httpx import AsyncClient

from tests.conftest import create_jwt


@pytest.mark.parametrize(
    "path, method",
    (
        ("/service-a/internal/users/50", HTTPMethod.GET),
        ("/service-a/internal/users/50/", HTTPMethod.PATCH),
        ("/service-a/internal/users/50", HTTPMethod.DELETE),
        ("/service-a/internal/users", HTTPMethod.POST),
        ("/service-a/internal/users/", HTTPMethod.GET),
        ("/test-service/internal/auth", HTTPMethod.GET),
    ),
)
async def test_internal_router_is_called(
    async_client: AsyncClient, path: str, method: HTTPMethod
):
    headers = {"Authorization": f"Bearer {create_jwt()}"}
    response = await async_client.request(method, path, headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Not authorized"}
