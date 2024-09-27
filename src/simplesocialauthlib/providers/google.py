import logging
from typing import Any, Final, cast, override

from google.auth.exceptions import GoogleAuthError
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from requests_oauthlib import OAuth2Session

from simplesocialauthlib.abstract import Providers, SocialAuthAbstract
from simplesocialauthlib.exceptions import CodeExchangeError, UserDataRetrievalError
from simplesocialauthlib.types import GoogleUserData
from simplesocialauthlib.utils import handle_request_exceptions

logger = logging.getLogger(__name__)


class GoogleSocialAuth(SocialAuthAbstract[GoogleUserData]):
    """
    Google authentication provider.

    This class implements the SocialAuthAbstract for Google OAuth2 authentication.
    It handles the OAuth2 flow and retrieves user data from Google.

    Attributes:
        client_id (str): The Google OAuth2 client ID.
        client_secret (str): The Google OAuth2 client secret.
        redirect_uri (str): The redirect URI for the OAuth2 flow.
        provider (Providers): The provider enum for Google.
        GOOGLE_SCOPES (list[str]): The scopes for Google OAuth2 authentication.
        GOOGLE_TOKEN_ENDPOINT (str): The endpoint for exchanging the authorization code for an access token.

    Example:
        auth = GoogleSocialAuth(client_id="your_id", client_secret="your_secret", redirect_uri="your_uri")\n
        user_data = auth.sign_in(code="received_code")
    """

    provider = Providers.GOOGLE
    GOOGLE_SCOPES: list[str] = [
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
    ]
    GOOGLE_TOKEN_ENDPOINT: Final[str] = "https://oauth2.googleapis.com/token"

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    @override
    @handle_request_exceptions("code exchange", CodeExchangeError)
    def exchange_code_for_access_token(self, code: str) -> str:
        oauth2_session = OAuth2Session(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            scope=GoogleSocialAuth.GOOGLE_SCOPES,
        )
        token = oauth2_session.fetch_token(
            token_url=GoogleSocialAuth.GOOGLE_TOKEN_ENDPOINT,
            client_secret=self.client_secret,
            code=code,
        )
        if "id_token" not in token:
            logger.error(f"Invalid token response: {token}")
            raise CodeExchangeError("Invalid token response: missing 'id_token'")
        return cast(str, token["id_token"])

    @override
    @handle_request_exceptions("user data retrieval", UserDataRetrievalError)
    def retrieve_user_data(self, access_token: str) -> GoogleUserData:
        try:
            id_info = cast(dict[str, Any], id_token.verify_oauth2_token(id_token=access_token, request=Request()))
            if "accounts.google.com" not in id_info.get("iss", ""):
                logger.error(f"Invalid token issuer: {id_info.get('iss')}")
                raise ValueError("Invalid token issuer")

            return GoogleUserData(
                first_name=id_info["given_name"],
                last_name=id_info["family_name"],
                full_name=id_info["name"],
                email=id_info["email"],
                picture=id_info.get("picture"),
                email_verified=id_info["email_verified"],
            )
        except GoogleAuthError as auth_err:
            logger.error(f"Google authentication error: {auth_err}")
            raise UserDataRetrievalError("Google authentication error") from auth_err
