import logging
from collections.abc import Callable
from typing import Any

from requests.exceptions import HTTPError, RequestException

logger = logging.getLogger(__name__)


def handle_request_exceptions(action: str, error_cls: type[Exception]) -> Callable[..., Callable[..., Any]]:
    """
    Handle common request exceptions for social auth providers.

    Args:
        action (str): The action being performed (e.g., 'code exchange', 'user data retrieval').
        error_cls (Exception): The exception class to raise (e.g., CodeExchangeError, UserDataRetrievalError).

    Returns:
        A function to be used as a decorator for handling exceptions.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Any:
            try:
                return func(*args, **kwargs)
            except HTTPError as http_err:
                logger.error(f"HTTP error during {action}: {http_err}")
                raise error_cls(f"HTTP error during {action}") from http_err
            except RequestException as req_err:
                logger.error(f"Request exception during {action}: {req_err}")
                raise error_cls(f"Request exception during {action}") from req_err
            except Exception as err:
                logger.error(f"Unexpected error during {action}: {err}")
                raise error_cls(f"Unexpected error during {action}") from err

        return wrapper

    return decorator
