from abc import ABC, abstractmethod
from enum import StrEnum
from typing import NoReturn


class Providers(StrEnum):
    APPLE = "apple"
    FACEBOOK = "facebook"
    GITHUB = "github"
    GOOGLE = "google"
    LINKEDIN = "linkedin"
    MICROSOFT = "microsoft"
    TWITTER = "twitter"


class SocialAuthAbstract(ABC):
    """
    Abstract class for social authentication.
    """

    provider: Providers

    @abstractmethod
    def exchange_code_for_access_token(self, code: str) -> str | NoReturn:
        """
        Exchange the authorization code for an access token.

        Args:
            code (str): The authorization code.

        Returns:
            str: The access token.

        Raises:
            ValueError: If the authorization code is invalid.
        """
        pass

    @abstractmethod
    def retrieve_user_data(self, access_token: str) -> dict | NoReturn:
        """
        Retrieve the user data from the social network.

        Args:
            access_token (str): The access token.

        Returns:
            dict: The user data.
        """
        pass
