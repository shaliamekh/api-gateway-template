class GatewayRouterException(Exception):
    def __str__(self) -> str:
        return "Something goes wrong. Please try again later"


class NotFoundException(Exception):
    def __str__(self) -> str:
        return "Not Found"
