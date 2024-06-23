from enum import StrEnum


class EnvType(StrEnum):
    test: str = "test"
    local: str = "local"
    dev: str = "dev"
    prod: str = "prod"
