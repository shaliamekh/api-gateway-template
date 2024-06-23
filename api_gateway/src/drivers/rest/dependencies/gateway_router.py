from typing import Annotated

import aiohttp
from fastapi import Depends

from adapters.aihttp_gateway_router import AiohttpGatewayRouter, get_session
from config.settings import BaseSettings, get_settings
from ports.gateway_router import GatewayRouter


def get_gateway_router(
    session: Annotated[aiohttp.ClientSession, Depends(get_session)],
    settings: Annotated[BaseSettings, Depends(get_settings)],
) -> GatewayRouter:
    return AiohttpGatewayRouter(session, settings)


# Create distinct dependencies for each handler to be
#  able to override a specific one when testing

get_generic_gateway_router = get_gateway_router
get_auth_gateway_router = get_gateway_router
get_openapi_gateway_router = get_gateway_router
