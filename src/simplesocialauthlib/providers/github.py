import logging
from typing import Final, cast, override

import requests

from simplesocialauthlib.abstract import Providers, SocialAuthAbstract
from simplesocialauthlib.exceptions import CodeExchangeError, UserDataRetrievalError
from simplesocialauthlib.types import GithubUserData
from simplesocialauthlib.utils import handle_request_exceptions

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

    provider: Providers = Providers.GITHUB
    GITHUB_TOKEN_ENDPOINT: Final[str] = "https://github.com/login/oauth/access_token"
    GITHUB_USER_INFO_ENDPOINT: Final[str] = "https://api.github.com/user"

    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

    @override
    @handle_request_exceptions("code exchange", CodeExchangeError)
    def exchange_code_for_access_token(self, code: str) -> str:
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
        }
        headers = {"Accept": "application/json"}
        response = requests.post(url=self.GITHUB_TOKEN_ENDPOINT, data=payload, headers=headers)
        response.raise_for_status()
        token_response = response.json()
        if "access_token" not in token_response:
            logger.error(f"Invalid token response: {token_response}")
            raise CodeExchangeError("Invalid token response: missing 'access_token'")
        return cast(str, token_response["access_token"])

    @override
    @handle_request_exceptions("user data retrieval", UserDataRetrievalError)
    def retrieve_user_data(self, access_token: str) -> GithubUserData:
        response = requests.get(
            url=self.GITHUB_USER_INFO_ENDPOINT,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        user_data = response.json()

        return GithubUserData(
            username=user_data["login"],
            full_name=user_data["name"],
            email=user_data["email"],
            picture=user_data["avatar_url"],
            bio=user_data.get("bio"),
            location=user_data.get("location"),
        )
