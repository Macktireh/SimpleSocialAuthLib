import logging
import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug import Response

from simplesocialauthlib.providers import GithubSocialAuth, GoogleSocialAuth

load_dotenv()

logging.basicConfig(level=logging.INFO)

app = Flask(import_name=__name__)
app.secret_key = os.environ["SECRET_KEY"]

# Initialise providers
google_auth = GoogleSocialAuth(
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    redirect_uri=os.environ["GOOGLE_REDIRECT_URI"],
)

github_auth = GithubSocialAuth(
    client_id=os.environ["GITHUB_CLIENT_ID"],
    client_secret=os.environ["GITHUB_CLIENT_SECRET"],
)


@app.route(rule="/", methods=["POST", "GET"])
def index() -> str:
    return render_template("index.html")


# --------------------------------------------------------------------------------
# ######  Sign in with Google Route
# --------------------------------------------------------------------------------
@app.route("/login/google/redirect", methods=["POST"])
def login_redirect_google() -> Response:
    """Redirects the user to Google for authentication."""
    if request.method != "POST":
        flash("Invalid request method.", category="danger")
        return redirect("/")

    authorization_url, state = google_auth.get_authorization_url()
    session["oauth_state"] = state
    return redirect(authorization_url)


@app.route(rule="/login/google/callback")
def login_callback_google() -> Response | str:
    """Callback after Google authentication."""
    code = request.args.get("code")
    received_state = request.args.get("state")
    saved_state = session.pop("oauth_state", None)

    if not code:
        flash("Authorization failed.", category="danger")
        return redirect("/")

    try:
        user_data = google_auth.sign_in(code=code, received_state=received_state, saved_state=saved_state)
        flash(f"Signed in with Google as {user_data['full_name']}.", category="success")
        return render_template(template_name_or_list="success.html", data=user_data, provider=google_auth.provider)
    except Exception as e:
        logging.error(e)
        flash("Something went wrong. Please try again.", category="danger")
        return redirect("/")


# --------------------------------------------------------------------------------
# ######  Sign in with Github Route
# --------------------------------------------------------------------------------
@app.route("/login/github/redirect", methods=["POST"])
def login_redirect_github() -> Response:
    """Redirects the user to GitHub for authentication."""
    if request.method != "POST":
        flash("Invalid request method.", category="danger")
        return redirect("/")

    authorization_url, state = github_auth.get_authorization_url()
    session["oauth_state"] = state
    return redirect(authorization_url)


@app.route(rule="/login/github/callback")
def login_callback_github() -> Response | str:
    """Callback after GitHub authentication."""
    code = request.args.get("code")
    received_state = request.args.get("state")
    saved_state = session.pop("oauth_state", None)

    if not code:
        flash("Authorization failed.", category="danger")
        return redirect("/")

    try:
        user_data = github_auth.sign_in(code=code, received_state=received_state, saved_state=saved_state)
        flash(f"Signed in with Github as {user_data['username']}.", category="success")
        return render_template(template_name_or_list="success.html", data=user_data, provider=github_auth.provider)
    except Exception as e:
        logging.error(e)
        flash("Something went wrong. Please try again.", category="danger")
        return redirect("/")


if __name__ == "__main__":
    DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")
    app.run(debug=DEBUG, host="localhost", port=5000)
