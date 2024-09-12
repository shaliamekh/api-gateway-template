from typing import Annotated, NoReturn

from fastapi import Depends, Request, Response

from drivers.rest.dependencies.gateway_router import get_generic_gateway_router
from drivers.rest.dependencies.security import validate_token
from drivers.rest.utils.api_router import APIRouter
from drivers.rest.utils.http_methods import ALL_METHODS
from ports.gateway_router import GatewayRouter
from use_cases.exceptions import ForbiddenException

router = APIRouter()


@router.api_route(
    "/{service}/internal/{path:path}/", methods=ALL_METHODS, response_model=None
)
async def internal_handler() -> NoReturn:
    raise ForbiddenException


@router.api_route(
    "/{service}/{path:path}",
    methods=ALL_METHODS,
    dependencies=[Depends(validate_token)],
)
async def generic_handler(
    service: str,
    path: str,
    request: Request,
    response: Response,
    redirect: Annotated[GatewayRouter, Depends(get_generic_gateway_router)],
) -> bytes:
    full_path = f"/{path}?{request.url.query}" if request.url.query else f"/{path}"
    body, response.status_code = await redirect(
        service, full_path, dict(request.headers), request.method, await request.body()
    )
    return body
