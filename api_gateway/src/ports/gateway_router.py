from abc import ABC, abstractmethod
from http import HTTPMethod
from typing import Any


class GatewayRouter(ABC):
    @abstractmethod
    async def __call__(
        self,
        service_name: str,
        route: str,
        headers: dict[str, Any],
        method: str = HTTPMethod.GET,
        body: bytes | None = None,
    ) -> tuple[bytes, int]:
        pass
