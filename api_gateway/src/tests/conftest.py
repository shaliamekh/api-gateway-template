from datetime import datetime, timedelta, timezone

import pytest
from jose import jwt
from pytest_asyncio import is_async_test

from config.settings import TestSettings


def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


def create_jwt(email: str | None = "test@example.com", ttl: int | None = 30) -> str:
    settings = TestSettings()
    payload = {}
    if ttl:
        payload["exp"] = datetime.now(tz=timezone.utc) + timedelta(seconds=ttl)
    if email:
        payload["aud"] = email  # type: ignore
    return jwt.encode(
        payload,
        settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )
