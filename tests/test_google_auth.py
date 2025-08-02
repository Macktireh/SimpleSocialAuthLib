from unittest.mock import MagicMock, patch

import pytest

from simplesocialauthlib.exceptions import (
    CodeExchangeError,
    TokenInvalidError,
    UserDataRetrievalError,
)
from simplesocialauthlib.providers.google import GoogleSocialAuth


@pytest.fixture
def google_auth() -> GoogleSocialAuth:
    """Fixture for GoogleSocialAuth."""
    return GoogleSocialAuth(
        client_id="test_id",
        client_secret="test_secret",
        redirect_uri="http://test.com/callback",
    )


@patch("simplesocialauthlib.providers.google.OAuth2Session")
def test_get_authorization_url(
    mock_oauth2_session: MagicMock, google_auth: GoogleSocialAuth
) -> None:
    """Test that get_authorization_url returns a valid URL and state."""
    mock_session_instance = MagicMock()
    mock_session_instance.authorization_url.return_value = (
        "https://auth.url/test",
        "mock_state",
    )
    mock_oauth2_session.return_value = mock_session_instance

    url, state = google_auth.get_authorization_url()

    assert "https://auth.url/test" in url
    assert state is not None
    assert len(state) > 10  # A reasonable check for a non-empty state


@patch("simplesocialauthlib.providers.google.GoogleSocialAuth.retrieve_user_data")
@patch("simplesocialauthlib.providers.google.GoogleSocialAuth.exchange_code_for_access_token")
def test_sign_in_success(
    mock_exchange: MagicMock, mock_retrieve: MagicMock, google_auth: GoogleSocialAuth
) -> None:
    """Test the complete sign_in flow successfully."""
    mock_exchange.return_value = "test_access_token"
    mock_retrieve.return_value = {"full_name": "Test User", "email": "test@test.com"}
    test_state = "super_secret_state"

    user_data = google_auth.sign_in(
        code="test_code", received_state=test_state, saved_state=test_state
    )

    mock_exchange.assert_called_once_with(code="test_code")
    mock_retrieve.assert_called_once_with(access_token="test_access_token")
    assert user_data["full_name"] == "Test User"


def test_sign_in_state_mismatch(google_auth: GoogleSocialAuth) -> None:
    """Test that sign_in fails if the state does not match."""
    with pytest.raises(TokenInvalidError, match="State parameter mismatch"):
        google_auth.sign_in(
            code="test_code",
            received_state="state_from_url",
            saved_state="state_from_session",
        )


def test_sign_in_state_missing(google_auth: GoogleSocialAuth) -> None:
    """Test that sign_in fails if the state is missing."""
    with pytest.raises(TokenInvalidError, match="State parameter is missing"):
        google_auth.sign_in(code="test_code", received_state="some_state", saved_state=None)


@patch(
    "simplesocialauthlib.providers.google.GoogleSocialAuth.exchange_code_for_access_token",
    side_effect=CodeExchangeError("Failed to exchange code"),
)
def test_sign_in_code_exchange_failure(
    mock_exchange: MagicMock, google_auth: GoogleSocialAuth
) -> None:
    """Test that sign_in fails if code exchange fails."""
    test_state = "super_secret_state"
    with pytest.raises(CodeExchangeError):
        google_auth.sign_in(code="bad_code", received_state=test_state, saved_state=test_state)


@patch("simplesocialauthlib.providers.google.GoogleSocialAuth.exchange_code_for_access_token")
@patch(
    "simplesocialauthlib.providers.google.GoogleSocialAuth.retrieve_user_data",
    side_effect=UserDataRetrievalError("Failed to get user"),
)
def test_sign_in_user_data_retrieval_failure(
    mock_retrieve: MagicMock, mock_exchange: MagicMock, google_auth: GoogleSocialAuth
) -> None:
    """Test that sign_in fails if user data retrieval fails."""
    mock_exchange.return_value = "test_access_token"
    test_state = "super_secret_state"
    with pytest.raises(UserDataRetrievalError):
        google_auth.sign_in(code="test_code", received_state=test_state, saved_state=test_state)
