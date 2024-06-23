from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from config.settings import BaseSettings, get_settings
from drivers.rest.utils.auth_schema import oauth_scheme
from use_cases.security import JWTValidator


def validate_token(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(oauth_scheme)],
    settings: Annotated[BaseSettings, Depends(get_settings)],
) -> None:
    JWTValidator(settings).validate(credentials.credentials if credentials else None)
