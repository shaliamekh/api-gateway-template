from http import HTTPMethod, HTTPStatus

import aiohttp
import pytest

from adapters.aihttp_gateway_router import AiohttpGatewayRouter
from adapters.exceptions import GatewayRouterException, NotFoundException
from config.settings import TestSettings


@pytest.fixture
def gateway_router(http_session: aiohttp.ClientSession):
    return AiohttpGatewayRouter(http_session, TestSettings())


@pytest.mark.asyncio
async def test_gateway_router_get(gateway_router):
    json_response, status_code = await gateway_router("test", "/posts/1", {})
    assert status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_gateway_router_post(gateway_router):
    data = b'{"title": "foo", "body": "bar", "userId": 1}'
    json_response, status_code = await gateway_router(
        "test", "/posts", {}, HTTPMethod.POST, data
    )
    assert status_code == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_gateway_router_patch(gateway_router):
    data = b'{"title": "new title"}'
    json_response, status_code = await gateway_router(
        "test", "/posts/1", {}, HTTPMethod.PATCH, data
    )
    assert status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_gateway_router_delete(gateway_router):
    json_response, status_code = await gateway_router(
        "test", "/posts/1", {}, HTTPMethod.DELETE
    )
    assert status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_gateway_router_not_found(gateway_router):
    json_response, status_code = await gateway_router("test", "/random/1", {})
    assert status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_gateway_router_service_not_responding(
    gateway_router, http_session: aiohttp.ClientSession
):
    with pytest.raises(GatewayRouterException):
        await gateway_router("not-exist", "/random/1", {})


@pytest.mark.asyncio
async def test_gateway_router_service_not_in_the_mapping(
    gateway_router, http_session: aiohttp.ClientSession
):
    with pytest.raises(NotFoundException):
        await gateway_router("random", "/random/1", {})
