from typing import Annotated

from fastapi import Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

from config.settings import BaseSettings, get_settings
from drivers.rest.utils.api_router import APIRouter

router = APIRouter()

templates = Jinja2Templates(directory=str(get_settings().base_path / "templates"))


@router.get("/", response_class=HTMLResponse)
@router.get("/docs", response_class=HTMLResponse)
async def index(
    request: Request, settings: Annotated[BaseSettings, Depends(get_settings)]
) -> _TemplateResponse:
    context = {
        "services": list(settings.service_mapping.values()),
        "api_gateway_url": settings.api_gateway_url,
    }
    return templates.TemplateResponse(
        request=request, name="index.html", context=context
    )


@router.get("/healthcheck")
def healthcheck() -> JSONResponse:
    return JSONResponse(content={"status": "OK"})
