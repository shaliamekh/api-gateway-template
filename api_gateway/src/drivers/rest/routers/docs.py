from http import HTTPMethod
from typing import Annotated

from fastapi import Depends, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, JSONResponse

from drivers.rest.dependencies.gateway_router import get_openapi_gateway_router
from drivers.rest.utils.api_router import APIRouter
from ports.gateway_router import GatewayRouter
from use_cases.docs import modify_paths

router = APIRouter()


@router.get("/{service}/docs")
async def docs_handler(service: str) -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url=f"/{service}/openapi.json",
        title=service.replace("-", " ").title(),
        swagger_favicon_url="/static/favicon.png",
    )


@router.get("/{service}/openapi.json")
async def openapi_handler(
    service: str,
    request: Request,
    redirect: Annotated[GatewayRouter, Depends(get_openapi_gateway_router)],
) -> JSONResponse:
    body, _ = await redirect(
        service, "/openapi.json", dict(request.headers), HTTPMethod.GET
    )
    return JSONResponse(content=modify_paths(body, service))
