from typing import Annotated, TypedDict


class GoogleUserData(TypedDict):
    first_name: Annotated[str, "Corresponds to 'given_name' in Google API"]
    last_name: Annotated[str, "Corresponds to 'family_name' in Google API"]
    full_name: Annotated[str | None, "Corresponds to 'name' in Google API"]
    email: Annotated[str, "Corresponds to 'email' in Google API"]
    email_verified: Annotated[bool, "Corresponds to 'email_verified' in Google API"]
    picture: Annotated[str | None, "Corresponds to 'picture' in Google API"]


class GithubUserData(TypedDict):
    username: Annotated[str, "Corresponds to 'login' in GitHub API"]
    full_name: Annotated[str, "Corresponds to 'name' in GitHub API"]
    email: Annotated[str, "Corresponds to 'email' in GitHub API"]
    picture: Annotated[str | None, "Corresponds to 'avatar_url' in GitHub API"]
    bio: Annotated[str | None, "Corresponds to 'bio' in GitHub API"]
    location: Annotated[str | None, "Corresponds to 'location' in GitHub API"]
