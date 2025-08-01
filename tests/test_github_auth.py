from unittest.mock import MagicMock, patch

import pytest

from simplesocialauthlib.exceptions import (
    CodeExchangeError,
    TokenInvalidError,
    UserDataRetrievalError,
)
from simplesocialauthlib.providers.github import GithubSocialAuth


@pytest.fixture
def github_auth() -> GithubSocialAuth:
    """Fixture for GithubSocialAuth."""
    return GithubSocialAuth(client_id="test_id", client_secret="test_secret")


def test_get_authorization_url(github_auth: GithubSocialAuth) -> None:
    """Test that get_authorization_url returns a valid URL and state."""
    url, state = github_auth.get_authorization_url()

    assert github_auth.GITHUB_AUTHORIZATION_URL in url
    assert f"client_id={github_auth.client_id}" in url
    assert "state=" in url
    assert state is not None
    assert len(state) > 10


@patch("simplesocialauthlib.providers.github.GithubSocialAuth.retrieve_user_data")
@patch("simplesocialauthlib.providers.github.GithubSocialAuth.exchange_code_for_access_token")
def test_sign_in_success(
    mock_exchange: MagicMock, mock_retrieve: MagicMock, github_auth: GithubSocialAuth
) -> None:
    """Test the complete sign_in flow successfully."""
    mock_exchange.return_value = "test_access_token"
    mock_retrieve.return_value = {"username": "Test User", "email": "test@test.com"}
    test_state = "super_secret_state"

    user_data = github_auth.sign_in(
        code="test_code", received_state=test_state, saved_state=test_state
    )

    mock_exchange.assert_called_once_with(code="test_code")
    mock_retrieve.assert_called_once_with(access_token="test_access_token")
    assert user_data["username"] == "Test User"


def test_sign_in_state_mismatch(github_auth: GithubSocialAuth) -> None:
    """Test that sign_in fails if the state does not match."""
    with pytest.raises(TokenInvalidError, match="State parameter mismatch"):
        github_auth.sign_in(
            code="test_code",
            received_state="state_from_url",
            saved_state="state_from_session",
        )


@patch(
    "simplesocialauthlib.providers.github.GithubSocialAuth.exchange_code_for_access_token",
    side_effect=CodeExchangeError("Failed to exchange code"),
)
def test_sign_in_code_exchange_failure(
    mock_exchange: MagicMock, github_auth: GithubSocialAuth
) -> None:
    """Test that sign_in fails if code exchange fails."""
    test_state = "super_secret_state"
    with pytest.raises(CodeExchangeError):
        github_auth.sign_in(code="bad_code", received_state=test_state, saved_state=test_state)


@patch("simplesocialauthlib.providers.github.GithubSocialAuth.exchange_code_for_access_token")
@patch(
    "simplesocialauthlib.providers.github.GithubSocialAuth.retrieve_user_data",
    side_effect=UserDataRetrievalError("Failed to get user"),
)
def test_sign_in_user_data_retrieval_failure(
    mock_retrieve: MagicMock, mock_exchange: MagicMock, github_auth: GithubSocialAuth
) -> None:
    """Test that sign_in fails if user data retrieval fails."""
    mock_exchange.return_value = "test_access_token"
    test_state = "super_secret_state"
    with pytest.raises(UserDataRetrievalError):
        github_auth.sign_in(code="test_code", received_state=test_state, saved_state=test_state)
