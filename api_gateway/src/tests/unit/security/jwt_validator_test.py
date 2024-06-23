import pytest

from config.settings import TestSettings
from tests.conftest import create_jwt
from use_cases.exceptions import (
    InvalidJWTException,
    JWTClaimsMissingException,
    JWTMissingException,
)
from use_cases.security import JWTValidator


@pytest.fixture
def jwt_validator() -> JWTValidator:
    return JWTValidator(TestSettings())


def test_jwt_validation_success(jwt_validator: JWTValidator):
    token = create_jwt()
    jwt_validator.validate(token)


def test_jwt_validation_expired(jwt_validator: JWTValidator):
    token = create_jwt(ttl=-30)
    with pytest.raises(InvalidJWTException):
        jwt_validator.validate(token)


def test_jwt_validation_exp_missing(jwt_validator: JWTValidator):
    token = create_jwt(ttl=None)
    with pytest.raises(JWTClaimsMissingException):
        jwt_validator.validate(token)


def test_jwt_validation_aud_missing(jwt_validator: JWTValidator):
    token = create_jwt(email=None)
    with pytest.raises(JWTClaimsMissingException):
        jwt_validator.validate(token)


def test_jwt_validation_token_missing(jwt_validator: JWTValidator):
    with pytest.raises(JWTMissingException):
        jwt_validator.validate(None)
