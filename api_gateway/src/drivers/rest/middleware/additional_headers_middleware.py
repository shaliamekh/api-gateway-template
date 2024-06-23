from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class AdditionalHeadersMiddleware:
    def __init__(self, app: ASGIApp, headers: dict[str, str]) -> None:
        self.app = app
        self.custom_headers = headers

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_wrapper(message: Message) -> None:
            if not message.get("headers"):
                message["headers"] = []
            headers = MutableHeaders(scope=message)
            for k, v in self.custom_headers.items():
                headers.append(k, v)
            await send(message)

        await self.app(scope, receive, send_wrapper)
