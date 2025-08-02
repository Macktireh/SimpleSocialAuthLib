__all__ = []

try:
    from simplesocialauthlib.providers.github import GithubSocialAuth

    __all__.append("GithubSocialAuth")
except ImportError:
    pass

try:
    from simplesocialauthlib.providers.google import GoogleSocialAuth

    __all__.append("GoogleSocialAuth")
except ImportError:
    pass


def _importerror_factory(provider_name: str, install_command: str):
    def raiser(*args, **kwargs):
        raise ImportError(
            f"The '{provider_name}' provider is not available because its dependencies are not installed.\n"  # noqa: E501
            f"Please run: pip install {install_command}"
        )

    return raiser


if "GithubSocialAuth" not in __all__:
    GithubSocialAuth = _importerror_factory("github", "simplesocialauthlib[github]")
    __all__.append("GithubSocialAuth")


if "GoogleSocialAuth" not in __all__:
    GoogleSocialAuth = _importerror_factory("google", "simplesocialauthlib[google]")
    __all__.append("GoogleSocialAuth")
