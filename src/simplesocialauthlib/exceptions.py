from typing import Any


class ApplicationError(Exception):
    def __init__(self, message: str, extra: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.extra = extra or {}


class TokenInvalidError(ApplicationError):
    pass


class CodeExchangeError(ApplicationError):
    pass


class UserDataRetrievalError(ApplicationError):
    pass


class ConfigurationError(ApplicationError):
    pass
