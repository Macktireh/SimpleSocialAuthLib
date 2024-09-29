# SimpleSocialAuthLib

SimpleSocialAuthLib is a Python library designed to simplify social authentication for various providers. It offers a straightforward interface for handling OAuth2 flows and retrieving user data from popular social platforms.

## Contents

- [Why use SimpleSocialAuthLib?](#why-use-simplesocialauthlib)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Returned Data Structure and OAuth URLs](#returned-data-structure-and-oauth-urls)
- [Full Example](#full-example)
- [Contributing](#contributing)
- [License](#license)

## Why use SimpleSocialAuthLib?

- **Simplicity**: Offers a clean and intuitive API for social authentication.
- **Flexibility**: Supports multiple social providers with a consistent interface.
- **Type Safety**: Utilizes Python type hints for better code quality and IDE support.
- **Extensibility**: Easily add new social providers by extending the base classes.

## Supported Social Providers

- [x] Google
- [x] GitHub

## Installation

Install SimpleSocialAuthLib:

```bash
# using pip
pip install simplesocialauthlib

# using pdm
pdm add simplesocialauthlib

# using uv
uv add simplesocialauthlib
```

## Configuration

Before using SimpleSocialAuthLib, you need to set up your social provider credentials. Here's how to configure for Google and GitHub:

### Google

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the Google+ API.
4. Create OAuth 2.0 credentials (client ID and client secret).
5. Set up the authorized redirect URIs.

### GitHub

1. Go to your [GitHub Developer Settings](https://github.com/settings/developers).
2. Click on "New OAuth App".
3. Fill in the application details, including the callback URL.
4. Once created, you'll get a client ID and can generate a client secret.

## Usage

Here's a basic example of how to use SimpleSocialAuthLib with Google authentication:

```python
from simplesocialauthlib.providers.google import GoogleSocialAuth

# Initialize the Google auth provider
google_auth = GoogleSocialAuth(
    client_id="your_google_client_id",
    client_secret="your_google_client_secret",
    redirect_uri="your_redirect_uri"
)

# After receiving the code from Google's OAuth redirect
code = "received_authorization_code"

# Complete the sign-in process
user_data = google_auth.sign_in(code=code)

# Use the user data as needed
print(f"Welcome, {user_data['full_name']}!")
```

## Returned Data Structure and OAuth URLs

### Google

**OAuth URL**:
```
https://accounts.google.com/o/oauth2/v2/auth?redirect_uri={{ GOOGLE_REDIRECT_URI }}&prompt=consent&response_type=code&client_id={{ GOOGLE_CLIENT_ID }}&scope=openid%20email%20profile&access_type=offline
```

**User Data Structure**:
```python
class GoogleUserData(TypedDict):
    first_name: str
    last_name: str
    full_name: str
    email: str
    email_verified: bool
    picture: str | None
```

### GitHub

**OAuth URL**:
```
https://github.com/login/oauth/authorize/?client_id={{ GITHUB_CLIENT_ID }}
```

**User Data Structure**:
```python
class GithubUserData(TypedDict):
    username: str
    full_name: str
    email: str
    picture: str | None
    bio: str | None
    location: str | None
```

## Full Example

Here's a full example using Flask to implement social login with both Google and GitHub:

```python
# app.py

import os
import logging

from flask import Flask, request, redirect, flash, render_template
from dotenv import load_dotenv

from simplesocialauthlib.providers.google import GoogleSocialAuth
from simplesocialauthlib.providers.github import GithubSocialAuth

load_dotenv()
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]


@app.route("/login")
def login():
    return render_template(
        "login.html",
        GOOGLE_CLIENT_ID=os.environ["GOOGLE_CLIENT_ID"],
        GOOGLE_REDIRECT_URI=os.environ["GOOGLE_REDIRECT_URI"],
        GITHUB_CLIENT_ID=os.environ["GITHUB_CLIENT_ID"],
    )


@app.route("/login/google")
def sign_in_with_google():
    code = request.args.get("code")
    if not code:
        return redirect("/login")

    try:
        google_auth = GoogleSocialAuth(
            client_id=os.environ["GOOGLE_CLIENT_ID"],
            client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
            redirect_uri=os.environ["GOOGLE_REDIRECT_URI"]
        )
        user_data = google_auth.sign_in(code=code)
        # Process user_data (e.g., create/update user in your database)
        flash("You are now signed in with Google.", category="success")
        return redirect("/")
    except Exception as e:
        logging.error(e)
        flash("Something went wrong. Please try again.", category="danger")
        return redirect("/login")


@app.route("/login/github")
def sign_in_with_github():
    code = request.args.get("code")
    if not code:
        return redirect("/login")

    try:
        github_auth = GithubSocialAuth(
            client_id=os.environ["GITHUB_CLIENT_ID"],
            client_secret=os.environ["GITHUB_CLIENT_SECRET"]
        )
        user_data = github_auth.sign_in(code=code)
        # Process user_data (e.g., create/update user in your database)
        flash("You are now signed in with Github.", category="success")
        return redirect("/")
    except Exception as e:
        logging.error(e)
        flash("Something went wrong. Please try again.", category="danger")
        return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
```

```html
<!-- login.html -->

...

<div class="d-grid gap-3 mx-auto" style="max-width: 320px;">
  <!-- Google -->
  <a
    href="https://accounts.google.com/o/oauth2/v2/auth?redirect_uri={{ GOOGLE_REDIRECT_URI }}&prompt=consent&response_type=code&client_id={{ GOOGLE_CLIENT_ID }}&scope=openid%20email%20profile&access_type=offline"
  >
    <span>Login with Google</span>
  </a>

  <!-- Github -->
  <a
    href="https://github.com/login/oauth/authorize/?client_id={{ GITHUB_CLIENT_ID }}"
  >
    <span>Login with Github</span>
  </a>
</div>

...

```

## Contributing

Contributions to SimpleSocialAuthLib are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
