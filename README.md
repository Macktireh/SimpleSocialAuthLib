<h1 align="center">🔐 SimpleSocialAuthLib #️⃣</h1>

<p align="center">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT" />
    <img src="https://codecov.io/gh/Macktireh/SimpleSocialAuthLib/branch/main/graph/badge.svg?token=41GGNZR0PC" alt="codecov" />
</p>

SimpleSocialAuthLib is a Python library designed to simplify social authentication. It offers a secure and straightforward interface for handling OAuth2 flows and retrieving user data from popular social platforms.

## Why use SimpleSocialAuthLib?

- **Simplicity**: Offers a clean and intuitive API for a complex process.
- **Flexibility**: Supports multiple social providers with a consistent interface.
- **Type Safety**: Utilizes Python type hints for better code quality and IDE support.
- **Extensibility**: Easily add new social providers by extending the base classes.
- **Security**: Incorporates state parameter verification to protect against Cross-Site Request Forgery (CSRF) attacks during the OAuth2 flow.

## Supported Social Providers

- [x] Google
- [x] GitHub
- [ ] Twitter/X
- [ ] LinkedIn

## Installation

You can install SimpleSocialAuthLib using your preferred Python package manager:

### Using pip

```bash
# Install the library with all providers and dependencies
pip install simplesocialauthlib[all]

# Or install specific providers
pip install simplesocialauthlib[github]  # For GitHub
pip install simplesocialauthlib[google]  # For Google
pip install simplesocialauthlib[github,google]  # For both GitHub and Google
```

### Using PDM

```bash
# Install the library with all providers and dependencies
pdm add simplesocialauthlib[all]

# Or install specific providers
pdm add simplesocialauthlib[github]  # For GitHub
pdm add simplesocialauthlib[google]  # For Google
pdm add simplesocialauthlib[github,google]  # For both GitHub and Google
```

### Using UV

```bash
# Install the library with all providers and dependencies
uv add simplesocialauthlib[all]

# Or install specific providers
uv add simplesocialauthlib[github]  # For GitHub
uv add simplesocialauthlib[google]  # For Google
uv add simplesocialauthlib[github,google]  # For both GitHub and Google
```

## Configuration

Before using the library, you need to obtain OAuth2 credentials (a Client ID and a Client Secret) from your chosen provider.

### Google

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project or select an existing one.
3.  In "APIs & Services" > "Credentials", create "OAuth 2.0 Client IDs".
4.  Select "Web application" as the application type.
5.  Add your authorized redirect URI (e.g., `http://localhost:5000/login/google/callback`). This is the URL the user will be sent to after authenticating with Google.
6.  Copy the **Client ID** and **Client Secret**.

### GitHub

1.  Go to your [GitHub Developer Settings](https://github.com/settings/developers) and select "OAuth Apps".
2.  Click on "New OAuth App".
3.  Fill in the application details. The "Authorization callback URL" is your redirect URI (e.g., `http://localhost:5000/login/github/callback`).
4.  Once created, copy the **Client ID** and generate a **Client Secret**.

## How It Works: The Secure OAuth2 Flow

This library enforces a secure authentication flow to protect your users:

1.  **Authorization Request**: Your application calls `get_authorization_url()` on a provider instance. This generates a unique URL for the user to visit and a secret `state` token.
2.  **Save the State**: Your application must save this `state` token in the user's session.
3.  **User Authentication**: The user is redirected to the provider (e.g., Google), where they approve the access request.
4.  **Callback**: The provider redirects the user back to your specified "callback URL" with an `authorization_code` and the `state` token.
5.  **Verification and Sign-In**: Your application calls `sign_in()`, passing the `code`, the `state` received from the provider, and the `state` you saved in the session. The library first verifies that the states match (preventing CSRF attacks) and then exchanges the code for user data.

## Usage

Here is a full example using **Flask** to implement social login with Google and GitHub.

```python
# app.py

import os
import logging

from flask import Flask, request, redirect, flash, render_template, session, url_for
from dotenv import load_dotenv

from simplesocialauthlib.providers import GithubSocialAuth, GoogleSocialAuth

# Load environment variables from .env file
load_dotenv()
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
# A secret key is required for Flask session management
app.secret_key = os.environ.get("SECRET_KEY", "a-strong-default-secret-key-for-dev")

# --- Initialize Providers ---
# It's best practice to initialize these once when the app starts.
google_auth = GoogleSocialAuth(
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    redirect_uri=os.environ["GOOGLE_REDIRECT_URI"],
)

github_auth = GithubSocialAuth(
    client_id=os.environ["GITHUB_CLIENT_ID"],
    client_secret=os.environ["GITHUB_CLIENT_SECRET"],
)


# --- Template Routes ---
@app.route("/")
def index():
    return "Welcome! You are not signed in. <a href='/login'>Login</a>"

@app.route("/login")
def login():
    return render_template("login.html")


# --- Google Authentication Flow ---
@app.route("/login/google", methods=["POST"])
def login_redirect_google():
    """Redirect user to Google's authorization page."""
    if request.method != "POST":
        flash("Invalid request method.", "danger")
        return redirect("/")

    authorization_url, state = google_auth.get_authorization_url()
    session["oauth_state"] = state
    return redirect(authorization_url)


@app.route("/login/google/callback")
def callback_google():
    """Handle the callback from Google."""
    code = request.args.get("code")
    received_state = request.args.get("state")
    saved_state = session.pop("oauth_state", None)

    try:
        # Verify state and sign in
        user_data = google_auth.sign_in(
            code=code, received_state=received_state, saved_state=saved_state
        )
        # At this point, you have the user's data.
        # You can create a user account, log them in, etc.
        flash(f"Successfully signed in with Google as {user_data['full_name']}.", "success")
        return redirect("/")

    except Exception as e:
        logging.error(f"Google auth failed: {e}")
        flash(f"Authentication failed: {e}", "danger")
        return redirect(url_for("login"))


# --- GitHub Authentication Flow ---
@app.route("/login/github", methods=["POST"])
def login_redirect_github():
    """Redirect user to GitHub's authorization page."""
    if request.method != "POST":
        flash("Invalid request method.", "danger")
        return redirect("/")

    authorization_url, state = github_auth.get_authorization_url()
    session["oauth_state"] = state
    return redirect(authorization_url)


@app.route("/login/github/callback")
def callback_github():
    """Handle the callback from GitHub."""
    code = request.args.get("code")
    received_state = request.args.get("state")
    saved_state = session.pop("oauth_state", None)

    try:
        # Verify state and sign in
        user_data = github_auth.sign_in(
            code=code, received_state=received_state, saved_state=saved_state
        )
        # At this point, you have the user's data.
        # You can create a user account, log them in, etc.
        flash(f"Successfully signed in with GitHub as {user_data['username']}.", "success")
        return redirect("/")

    except Exception as e:
        logging.error(f"GitHub auth failed: {e}")
        flash(f"Authentication failed: {e}", "danger")
        return redirect(url_for("login"))


if __name__ == "__main__":
    # Ensure you are not running in debug mode in production!
    # The callback must use HTTPS in production.
    app.run(debug=True, port=5000)
```

```html
<!-- templates/login.html -->

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-a" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Login</title>
  </head>
  <body>
    <h1>Login with a social provider</h1>

    <form method="POST" action="{{ url_for('login_redirect_google') }}">
      <button
          type="submit"
          class="btn btn-outline-primary w-100 d-flex justify-content-center align-items-center gap-1 btn-hover-opacity"
      >
        Login with Google
      </button>
    </form>

    <form method="POST" action="{{ url_for('login_redirect_github') }}">
      <button
          type="submit"
          class="btn btn-outline-primary w-100 d-flex justify-content-center align-items-center gap-1 btn-hover-opacity"
      >
        Login with Github
      </button>
    </form>
  </body>
</html>
```

## Returned Data Structure

The `sign_in` method returns a `TypedDict` with a normalized structure.

### Google `GoogleUserData`

```python
class GoogleUserData(TypedDict):
    first_name: str
    last_name: str
    full_name: str
    email: str
    email_verified: bool
    picture: str | None
```

### GitHub `GithubUserData`

```python
class GithubUserData(TypedDict):
    username: str
    full_name: str | None
    email: str | None
    picture: str | None
    bio: str | None
    location: str | None
```

## Contributing

We welcome contributions to SimpleSocialAuthLib\! If you'd like to contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Implement your changes, ensuring they adhere to the existing code style and conventions.
4.  Write comprehensive tests for your new features or bug fixes.
5.  Update the documentation to reflect any changes in functionality or API.
6.  Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License.
