from abc import ABC, abstractmethod
from collections.abc import Mapping
from enum import StrEnum
from typing import Any, Generic, TypeVar

T = TypeVar("T", bound=Mapping[str, Any])


class Providers(StrEnum):
    APPLE = "apple"
    FACEBOOK = "facebook"
    GITHUB = "github"
    GOOGLE = "google"
    LINKEDIN = "linkedin"
    MICROSOFT = "microsoft"
    TWITTER = "twitter"


class SocialAuthAbstract(ABC, Generic[T]):
    """
    Abstract class for social authentication.

    This class defines the interface for all social authentication providers.
    Each provider should implement these methods according to their specific API.
    """

    provider: Providers

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

    def sign_in(self, code: str) -> T:
        """
        Complete the sign-in process by exchanging the code for a token and retrieving user data.

        Args:
            code (str): The authorization code received from the OAuth provider.

        Returns:
            T: The user data in a provider-specific format.

        Raises:
            CodeExchangeError: If the code exchange fails.
            UserDataRetrievalError: If the user data retrieval fails.
        """
        access_token = self.exchange_code_for_access_token(code=code)
        return self.retrieve_user_data(access_token=access_token)
