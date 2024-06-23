import typing
from http import HTTPStatus

from fastapi import Response
from starlette.background import BackgroundTask


class RowJSONResponse(Response):
    media_type = "application/json"

    def __init__(
        self,
        content: bytes,
        status_code: int = HTTPStatus.OK,
        headers: typing.Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        super().__init__(content, status_code, headers, media_type, background)
