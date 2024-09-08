from typing import Annotated, Required, TypedDict


"""
{'at_hash': 'ADXg-bC6BsI_RS082zq5xg',
 'aud': '245618730282-n8rappdah6ihq39583o0jlc76n7gs7du.apps.googleusercontent.com',
 'azp': '245618730282-n8rappdah6ihq39583o0jlc76n7gs7du.apps.googleusercontent.com',
 'email': 'clonetwitter256@gmail.com',
 'email_verified': True,
 'exp': 1725737372,
 'family_name': 'Twitter',
 'given_name': 'Clone',
 'iat': 1725733772,
 'iss': 'https://accounts.google.com',
 'name': 'Clone Twitter',
 'picture': 'https://lh3.googleusercontent.com/a/ACg8ocJnaFbKIeESNIvbuOTFkqox_6WzuysggejiHkrlcRdhkq3G-w=s96-c',
 'sub': '111516932344481023161'}
"""
class GoogleUserData(TypedDict):
    first_name: Annotated[Required[str], "Corresponds to 'given_name' in Google API"]
    last_name: Annotated[Required[str], "Corresponds to 'family_name' in Google API"]
    full_name: Annotated[str | None, "Corresponds to 'name' in Google API"]
    email: Annotated[Required[str], "Corresponds to 'email' in Google API"]
    email_verified: Annotated[bool | None, "Corresponds to 'email_verified' in Google API"]
    picture: Annotated[str | None, "Corresponds to 'picture' in Google API"]


class GithubUserData(TypedDict):
    username: Annotated[Required[str], "Corresponds to 'login' in GitHub API"]
    full_name: Annotated[Required[str], "Corresponds to 'name' in GitHub API"]
    email: Annotated[Required[str], "Corresponds to 'email' in GitHub API"]
    picture: Annotated[str | None, "Corresponds to 'avatar_url' in GitHub API"]
    bio: Annotated[str | None, "Corresponds to 'bio' in GitHub API"]
    location: Annotated[str | None, "Corresponds to 'location' in GitHub API"]
