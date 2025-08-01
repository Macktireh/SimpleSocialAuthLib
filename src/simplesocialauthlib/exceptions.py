from typing import Any


class ApplicationError(Exception):
    """Base exception for all errors raised by this library."""

    def __init__(self, message: str, extra: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.extra = extra or {}


class TokenInvalidError(ApplicationError):
    """Raised when a token (e.g., state, access token) is invalid, expired, or malformed."""

    pass


class CodeExchangeError(ApplicationError):
    """Raised when the exchange of an authorization code for an access token fails."""

    pass


class UserDataRetrievalError(ApplicationError):
    """Raised when fetching the user's profile data from the provider fails."""

    pass


class ConfigurationError(ApplicationError):
    """Raised for configuration-related issues, such as a missing redirect URI."""

    pass
