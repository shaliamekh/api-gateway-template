import logging
from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import SecretStr
from pydantic_settings import BaseSettings as PydanticBaseSettings

from config.environements import EnvType
from domain.enitities.service import Service


class BaseSettings(PydanticBaseSettings):
    env: EnvType
    api_gateway_url: str = "http://localhost:8010"
    service_a_url: str = "http://service-a:8000"
    service_b_url: str = "http://service-b:8000"
    log_level: int = logging.DEBUG
    jwt_secret_key: SecretStr = SecretStr("")
    jwt_algorithm: str = "HS256"
    allow_origins: list[str] = ["*"]
    additional_headers: dict[str, Any] = {
        "Strict-Transport-Security": "max-age=31536000",
        "X-Content-Type-Options": "nosniff",
    }
    base_path: Path = Path(__file__).parent.parent.resolve()

    def configure_logging(self) -> None:
        logging.basicConfig(level=self.log_level)

    @property
    def service_mapping(self) -> dict[str, Service]:
        return {
            "service-a": Service(
                name="Service A", internal_url=self.service_a_url, slag="service-a"
            ),
            "service-b": Service(
                name="Service B", internal_url=self.service_b_url, slag="service-b"
            ),
        }


class TestSettings(BaseSettings):
    env: EnvType = EnvType.test
    jwt_secret_key: SecretStr = SecretStr("supersecret")

    @property
    def service_mapping(self) -> dict[str, Service]:
        return {
            "test": Service(
                name="Test",
                internal_url="https://jsonplaceholder.typicode.com",
                slag="test",
            ),
            "not-exist": Service(
                name="Not exist", internal_url="https://not-exist", slag="not-exist"
            ),
        }


class LocalSettings(BaseSettings):
    pass


class DevSettings(BaseSettings):
    pass


class ProdSettings(BaseSettings):
    log_level: int = logging.INFO


settings_mapping = {
    EnvType.dev: DevSettings,
    EnvType.test: TestSettings,
    EnvType.prod: ProdSettings,
    EnvType.local: LocalSettings,
}


@lru_cache
def get_settings() -> BaseSettings:
    app_env = BaseSettings().env
    return settings_mapping[app_env]()
