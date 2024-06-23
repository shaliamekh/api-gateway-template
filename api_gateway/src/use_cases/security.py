from jose import jwt

from config.settings import BaseSettings
from use_cases.exceptions import (
    InvalidJWTException,
    JWTClaimsMissingException,
    JWTMissingException,
)


class JWTValidator:
    ALGORITHM = "HS256"

    def __init__(self, settings: BaseSettings):
        self.settings = settings

    def validate(self, access_token: str | None = None) -> None:
        if access_token is None:
            raise JWTMissingException
        try:
            claims = jwt.decode(
                access_token,
                self.settings.jwt_secret_key.get_secret_value(),
                algorithms=self.settings.jwt_algorithm,
                options={"verify_aud": False},
            )
        except Exception as e:
            raise InvalidJWTException from e
        if not claims.get("aud") or not claims.get("exp"):
            raise JWTClaimsMissingException
