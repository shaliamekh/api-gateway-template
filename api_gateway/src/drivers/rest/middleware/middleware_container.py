from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from config.settings import get_settings
from drivers.rest.middleware.additional_headers_middleware import (
    AdditionalHeadersMiddleware,
)


def middleware_container(app: FastAPI) -> None:
    # setting some additional security headers
    app.add_middleware(
        AdditionalHeadersMiddleware, headers=get_settings().additional_headers
    )

    # getting the connecting client information in case of the app being deployed behind a proxy
    app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=["*"])  # type: ignore

    # setting CORS
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_origins=get_settings().allow_origins,
    )
