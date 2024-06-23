from http import HTTPMethod
from typing import Annotated

from fastapi import Depends, Request, Response

from drivers.rest.dependencies.gateway_router import get_auth_gateway_router
from drivers.rest.utils.api_router import APIRouter
from ports.gateway_router import GatewayRouter

router = APIRouter()


@router.post("/service-a/auth/{path:path}")
async def auth_handler(
    path: str,
    request: Request,
    response: Response,
    redirect: Annotated[GatewayRouter, Depends(get_auth_gateway_router)],
) -> bytes:
    body, response.status_code = await redirect(
        "service-a",
        f"/auth/{path}",
        dict(request.headers),
        HTTPMethod.POST,
        await request.body(),
    )
    return body
