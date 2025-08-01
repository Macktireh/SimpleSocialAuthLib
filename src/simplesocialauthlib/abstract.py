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
    Abstract class for social authentication.

    This class defines the interface for all social authentication providers.
    Each provider should implement these methods according to their specific API.
    """

    provider: Providers

    def _generate_state(self) -> str:
        """Generates a secure random string for the state parameter."""
        return secrets.token_urlsafe(32)

    def _verify_state(self, received_state: str | None, saved_state: str | None) -> None:
        """
        Verifies that the received state matches the saved state.

        Raises:
            TokenInvalidError: If the states are missing or do not match.
        """
        if not received_state or not saved_state:
            raise TokenInvalidError("State parameter is missing in the request or session.")
        if not secrets.compare_digest(received_state, saved_state):
            raise TokenInvalidError("State parameter mismatch. Possible CSRF attack.")

    @abstractmethod
    def get_authorization_url(self) -> tuple[str, str]:
        """
        Generate the authorization URL and the state for the OAuth provider.

        The state should be stored in the user's session.

        Returns:
            tuple[str, str]: A tuple containing the authorization URL and the state.
        """
        pass

    @abstractmethod
    def exchange_code_for_access_token(self, code: str) -> str:
        """
        Exchange the authorization code for an access token.

        Args:
            code (str): The authorization code received from the OAuth provider.

        Returns:
            str: The access token.

        Raises:
            CodeExchangeError: If the authorization code is invalid or the exchange fails.
        """
        pass

    @abstractmethod
    def retrieve_user_data(self, access_token: str) -> T:
        """
        Retrieve the user data from the social network.

        Args:
            access_token (str): The access token obtained from exchange_code_for_access_token.

        Returns:
            T: The user data in a provider-specific format.

        Raises:
            UserDataRetrievalError: If the access token is invalid or the data retrieval fails.
        """
        pass

    def sign_in(self, *, code: str, received_state: str | None, saved_state: str | None) -> T:
        """
        Complete the sign-in process by verifying the state, exchanging the code,
        and retrieving user data.

        Args:
            code (str): The authorization code from the OAuth provider.
            received_state (str | None): The state parameter from the callback URL.
            saved_state (str | None): The state parameter saved in the user's session.

        Returns:
            T: The user data in a provider-specific format.

        Raises:
            TokenInvalidError: If the state verification fails.
            CodeExchangeError: If the code exchange fails.
            UserDataRetrievalError: If the user data retrieval fails.
        """
        self._verify_state(received_state=received_state, saved_state=saved_state)
        access_token = self.exchange_code_for_access_token(code=code)
        return self.retrieve_user_data(access_token=access_token)
