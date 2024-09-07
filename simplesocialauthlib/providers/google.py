import logging
from typing import override

from google.auth.transport.requests import Request
from google.oauth2 import id_token
from requests_oauthlib import OAuth2Session

from simplesocialauthlib.abstract import Providers, SocialAuthAbstract
from simplesocialauthlib.exceptions import CodeExchangeError, UserDataRetrievalError
from simplesocialauthlib.config import GOOGLE_SCOPES, GOOGLE_TOKEN_ENDPOINT
from simplesocialauthlib.types import GoogleUserData

logger = logging.getLogger(__name__)


class GoogleSocialAuth(SocialAuthAbstract[GoogleUserData]):
    """
    Google authentication provider.

    This class implements the SocialAuthAbstract for Google OAuth2 authentication.
    It handles the OAuth2 flow and retrieves user data from Google.

    Attributes:
        provider (Providers): The provider enum for Google.
        client_id (str): The Google OAuth2 client ID.
        client_secret (str): The Google OAuth2 client secret.
        redirect_uri (str): The redirect URI for the OAuth2 flow.

    Example:
        auth = GoogleSocialAuth(client_id="your_id", client_secret="your_secret", redirect_uri="your_uri")
        user_data = auth.sign_in(code="received_code")
    """

    provider = Providers.GOOGLE

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    @override
    def exchange_code_for_access_token(self, code: str) -> str:
        try:
            oauth2_session = OAuth2Session(
                client_id=self.client_id,
                redirect_uri=self.redirect_uri,
                scope=GOOGLE_SCOPES,
            )
            token = oauth2_session.fetch_token(
                token_url=GOOGLE_TOKEN_ENDPOINT,
                client_secret=self.client_secret,
                code=code,
            )
            return token["id_token"]
        except Exception as err:
            logger.error(f"Failed to exchange code for token: {err}")
            raise CodeExchangeError("Google authorization code is invalid") from err

    @override
    def retrieve_user_data(self, access_token: str) -> GoogleUserData:
        try:
            id_info = id_token.verify_oauth2_token(
                id_token=access_token,
                request=Request(),
                audience=self.client_id,
            )
            if "accounts.google.com" not in id_info["iss"]:
                raise ValueError("Wrong issuer")

            return GoogleUserData(
                first_name=id_info["given_name"],
                last_name=id_info["family_name"],
                full_name=id_info["name"],
                email=id_info["email"],
                picture=id_info.get("picture"),
                email_verified=id_info["email_verified"],
            )
        except Exception as err:
            logger.error(f"Failed to retrieve user data: {err}")
            raise UserDataRetrievalError(
                "Failed to retrieve or validate Google user data"
            ) from err
