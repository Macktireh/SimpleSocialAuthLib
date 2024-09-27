from unittest.mock import MagicMock, patch

import pytest

from simplesocialauthlib.exceptions import CodeExchangeError, UserDataRetrievalError
from simplesocialauthlib.providers.google import GoogleSocialAuth


@pytest.fixture
def google_auth() -> GoogleSocialAuth:
    return GoogleSocialAuth(client_id="test_id", client_secret="test_secret", redirect_uri="http://test.com/callback")


@patch("simplesocialauthlib.providers.google.OAuth2Session")
def test_exchange_code_for_access_token_success(mock_oauth2_session, google_auth: GoogleSocialAuth) -> None:
    mock_session = MagicMock()
    mock_session.fetch_token.return_value = {"id_token": "test_token"}
    mock_oauth2_session.return_value = mock_session

    result = google_auth.exchange_code_for_access_token("test_code")
    assert result == "test_token"


@patch("simplesocialauthlib.providers.google.OAuth2Session")
def test_exchange_code_for_access_token_failure(mock_oauth2_session, google_auth: GoogleSocialAuth) -> None:
    mock_session = MagicMock()
    mock_session.fetch_token.side_effect = Exception("Token fetch failed")
    mock_oauth2_session.return_value = mock_session

    with pytest.raises(CodeExchangeError):
        google_auth.exchange_code_for_access_token("test_code")


@patch("simplesocialauthlib.providers.google.id_token")
def test_retrieve_user_data_success(mock_id_token, google_auth: GoogleSocialAuth) -> None:
    mock_id_token.verify_oauth2_token.return_value = {
        "iss": "https://accounts.google.com",
        "given_name": "Test",
        "family_name": "User",
        "name": "Test User",
        "email": "test@example.com",
        "email_verified": True,
        "picture": "http://example.com/picture.jpg",
    }

    result = google_auth.retrieve_user_data("test_token")
    assert result["first_name"] == "Test"
    assert result["email"] == "test@example.com"


@patch("simplesocialauthlib.providers.google.id_token")
def test_retrieve_user_data_failure(mock_id_token, google_auth: GoogleSocialAuth) -> None:
    mock_id_token.verify_oauth2_token.side_effect = Exception("Token verification failed")

    with pytest.raises(UserDataRetrievalError):
        google_auth.retrieve_user_data("test_token")
