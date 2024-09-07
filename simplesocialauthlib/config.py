from typing import Final

GOOGLE_SCOPES: Final[list[str]] = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
]
GOOGLE_TOKEN_ENDPOINT: Final[str] = "https://oauth2.googleapis.com/token"

FACEBOOK_SCOPES: Final[list[str]] = ["email", "public_profile"]
FACEBOOK_TOKEN_ENDPOINT: Final[str] = "https://graph.facebook.com/v12.0/oauth/access_token"
FACEBOOK_USER_INFO_ENDPOINT: Final[str] = "https://graph.facebook.com/me"

# Ajoutez d'autres constantes pour les différents fournisseurs ici