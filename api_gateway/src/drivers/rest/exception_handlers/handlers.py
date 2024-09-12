from fastapi import Request, status
from fastapi.responses import JSONResponse, Response


def jwt_not_valid_exception_handler(request: Request, exc: Exception) -> Response:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
        headers={"WWW-Authenticate": "Bearer"},
    )


async def gateway_exception_handler(request: Request, exc: Exception) -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)}
    )


async def not_found_exception_handler(request: Request, exc: Exception) -> Response:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
    )


async def forbidden_exception_handler(request: Request, exc: Exception) -> Response:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN, content={"detail": str(exc)}
    )
