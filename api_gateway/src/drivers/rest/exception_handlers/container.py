from fastapi import FastAPI

from adapters.exceptions import GatewayRouterException, NotFoundException
from drivers.rest.exception_handlers.handlers import (
    forbidden_exception_handler,
    gateway_exception_handler,
    jwt_not_valid_exception_handler,
    not_found_exception_handler,
)
from use_cases.exceptions import ForbiddenException, NotAuthorizedException


def exception_container(app: FastAPI) -> None:
    app.add_exception_handler(NotAuthorizedException, jwt_not_valid_exception_handler)
    app.add_exception_handler(GatewayRouterException, gateway_exception_handler)
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(ForbiddenException, forbidden_exception_handler)
