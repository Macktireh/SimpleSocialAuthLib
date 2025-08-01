import secrets
from abc import ABC, abstractmethod
from collections.abc import Mapping
from enum import StrEnum
from typing import Any, TypeVar

from simplesocialauthlib.exceptions import TokenInvalidError

T = TypeVar("T", bound=Mapping[str, Any])


class Providers(StrEnum):
    APPLE = "apple"
    FACEBOOK = "facebook"
    GITHUB = "github"
    GOOGLE = "google"
    LINKEDIN = "linkedin"
    MICROSOFT = "microsoft"
    TWITTER = "twitter"


class SocialAuthAbstract[T: Mapping[str, Any]](ABC):
    """
    Abstract base class for social authentication providers.

    This class defines the public interface for handling an OAuth2 authentication
    flow in a secure manner. Each provider must implement the abstract methods
    to handle provider-specific details.

    The intended flow is:
    1. Call `get_authorization_url()` to get the URL to redirect the user to.
    2. Store the returned `state` in the user's session.
    3. After the user authenticates and is redirected back to your app,
       call `sign_in()` with the `code` and `state` from the callback URL,
       along with the `state` you saved in the session.
    """

    provider: Providers

    def _generate_state(self) -> str:
        """Generates a secure random string for the state parameter."""
        return secrets.token_urlsafe(32)

    def _verify_state(self, received_state: str | None, saved_state: str | None) -> None:
        """
        Verifies that the received state matches the saved state to prevent CSRF.

        Args:
            received_state: The state parameter from the provider's callback URL.
            saved_state: The state parameter stored in the user's session.

        Raises:
            TokenInvalidError: If states are missing or do not match.
        """
        if not received_state or not saved_state:
            raise TokenInvalidError("State parameter is missing in the request or session.")
        if not secrets.compare_digest(received_state, saved_state):
            raise TokenInvalidError("State parameter mismatch. Possible CSRF attack.")

    @abstractmethod
    def get_authorization_url(self) -> tuple[str, str]:
        """
        Generates the provider's authorization URL and a unique state parameter.

        The returned `state` must be stored in the user's session to be
        verified in the callback phase.

        Returns:
            A tuple containing:
            - str: The full authorization URL to redirect the user to.
            - str: The `state` token to store in the user's session.
        """
        pass

    @abstractmethod
    def exchange_code_for_access_token(self, code: str) -> str:
        """
        Exchanges an authorization code for an access token.

        Args:
            code: The authorization code received from the OAuth provider.

        Returns:
            The access token (or ID token for Google) as a string.

        Raises:
            CodeExchangeError: If the code is invalid or the exchange fails.
        """
        pass

    @abstractmethod
    def retrieve_user_data(self, access_token: str) -> T:
        """
        Retrieves user data from the provider using an access token.

        Args:
            access_token: The access token obtained from the code exchange.

        Returns:
            A TypedDict containing the user's information.

        Raises:
            UserDataRetrievalError: If the token is invalid or data retrieval fails.
        """
        pass

    def sign_in(self, *, code: str, received_state: str | None, saved_state: str | None) -> T:
        """
        Completes the sign-in process securely.

        This method first verifies the state to prevent CSRF attacks, then
        exchanges the authorization code for an access token, and finally
        retrieves the user's data.

        Args:
            code: The authorization code from the provider's callback URL.
            received_state: The state from the provider's callback URL.
            saved_state: The state that was previously stored in the user's session.

        Returns:
            A TypedDict containing the user's information.

        Raises:
            TokenInvalidError: If the state verification fails.
            CodeExchangeError: If the code exchange fails.
            UserDataRetrievalError: If the user data retrieval fails.
        """
        self._verify_state(received_state=received_state, saved_state=saved_state)
        access_token = self.exchange_code_for_access_token(code=code)
        return self.retrieve_user_data(access_token=access_token)
