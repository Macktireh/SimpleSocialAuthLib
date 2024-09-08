import logging
from typing import Final, override

import requests
from simplesocialauthlib.abstract import Providers, SocialAuthAbstract
from simplesocialauthlib.exceptions import CodeExchangeError, UserDataRetrievalError
from simplesocialauthlib.types import GithubUserData

logger = logging.getLogger(__name__)


class GithubSocialAuth(SocialAuthAbstract[GithubUserData]):
    """
    Github authentication provider.

    This class implements the SocialAuthAbstract for Github OAuth2 authentication.
    It handles the OAuth2 flow and retrieves user data from Github.

    Attributes:
        client_id (str): The Github OAuth2 client ID.
        client_secret (str): The Github OAuth2 client secret.
        provider (Providers): The provider enum for Github.
        GITHUB_TOKEN_ENDPOINT (str): The endpoint for exchanging the authorization code for an access token.
        GITHUB_USER_INFO_ENDPOINT (str): The endpoint for retrieving user data.

    Example:
        auth = GithubSocialAuth(client_id="your_id", client_secret="your_secret")\n
        user_data = auth.sign_in(code="received_code")
    """

    provider: Final[Providers] = Providers.GITHUB
    GITHUB_TOKEN_ENDPOINT: Final[str] = "https://github.com/login/oauth/access_token"
    GITHUB_USER_INFO_ENDPOINT: Final[str] = "https://api.github.com/user"

    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

    @override
    def exchange_code_for_access_token(self, code: str) -> str:
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
        }
        response = requests.post(url=self.GITHUB_TOKEN_ENDPOINT, data=payload)
        if response.status_code != 200:
            logger.error(f"Failed to exchange code for token: {response.text}")
            raise CodeExchangeError("Failed to exchange code for token")
        return response.json()["access_token"]

    @override
    def retrieve_user_data(self, access_token: str) -> GithubUserData:
        try:
            response = requests.get(
                url=self.GITHUB_USER_INFO_ENDPOINT,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if response.status_code != 200:
                raise UserDataRetrievalError("Failed to retrieve user data")
            return response.json()
        except Exception as err:
            logger.error(f"Failed to retrieve user data: {err}")
            raise UserDataRetrievalError("Failed to retrieve user data") from err
