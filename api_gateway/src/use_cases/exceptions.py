class NotAuthorizedException(Exception):
    def __str__(self) -> str:
        return "Not authorized"


class JWTMissingException(NotAuthorizedException):
    pass


class InvalidJWTException(NotAuthorizedException):
    pass


class JWTClaimsMissingException(NotAuthorizedException):
    pass
