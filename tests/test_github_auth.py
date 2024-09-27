from unittest.mock import MagicMock, patch

import pytest

from simplesocialauthlib.exceptions import CodeExchangeError, UserDataRetrievalError
from simplesocialauthlib.providers.github import GithubSocialAuth


@pytest.fixture
def github_auth() -> GithubSocialAuth:
    return GithubSocialAuth(client_id="test_id", client_secret="test_secret")


@patch("simplesocialauthlib.providers.github.requests.post")
def test_exchange_code_for_access_token_success(mock_post, github_auth: GithubSocialAuth) -> None:
    mock_response = MagicMock()
    mock_response.json.return_value = {"access_token": "test_token"}
    mock_post.return_value = mock_response

    result = github_auth.exchange_code_for_access_token("test_code")
    assert result == "test_token"


@patch("simplesocialauthlib.providers.github.requests.post")
def test_exchange_code_for_access_token_failure(mock_post, github_auth: GithubSocialAuth) -> None:
    mock_post.side_effect = Exception("Request failed")

    with pytest.raises(CodeExchangeError):
        github_auth.exchange_code_for_access_token("test_code")


@patch("simplesocialauthlib.providers.github.requests.get")
def test_retrieve_user_data_success(mock_get, github_auth: GithubSocialAuth) -> None:
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "login": "testuser",
        "name": "Test User",
        "email": "test@example.com",
        "avatar_url": "http://example.com/avatar.jpg",
        "bio": "Test bio",
        "location": "Test location",
    }
    mock_get.return_value = mock_response

    result = github_auth.retrieve_user_data("test_token")
    assert result["username"] == "testuser"
    assert result["email"] == "test@example.com"


@patch("simplesocialauthlib.providers.github.requests.get")
def test_retrieve_user_data_failure(mock_get, github_auth: GithubSocialAuth) -> None:
    mock_get.side_effect = Exception("Request failed")

    with pytest.raises(UserDataRetrievalError):
        github_auth.retrieve_user_data("test_token")
