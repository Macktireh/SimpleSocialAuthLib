from typing import TypedDict, Required


class GoogleUserData(TypedDict):
    first_name: Required[str]
    last_name: Required[str]
    full_name: str | None
    email: Required[str]
    email_verified: bool | None
    picture: str | None
