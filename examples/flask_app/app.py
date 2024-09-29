import logging
import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request

from simplesocialauthlib.providers.github import GithubSocialAuth
from simplesocialauthlib.providers.google import GoogleSocialAuth

load_dotenv()

logging.basicConfig(level=logging.INFO)

app = Flask(import_name=__name__)
app.secret_key = os.environ["SECRET_KEY"]


@app.route(rule="/")
def index() -> str:
    return render_template(
        template_name_or_list="index.html",
        GOOGLE_CLIENT_ID=os.environ["GOOGLE_CLIENT_ID"],
        GOOGLE_REDIRECT_URI=os.environ["GOOGLE_REDIRECT_URI"],
        GITHUB_CLIENT_ID=os.environ["GITHUB_CLIENT_ID"],
    )


# --------------------------------------------------------------------------------
# ######  Sign in with Google Route
# --------------------------------------------------------------------------------
@app.route(rule="/login/google")
def sign_in_with_google() -> str:
    code = request.args.get(key="code")

    try:
        google_auth = GoogleSocialAuth(
            client_id=os.environ["GOOGLE_CLIENT_ID"],
            client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
            redirect_uri=os.environ["GOOGLE_REDIRECT_URI"],
        )
        user_data = google_auth.sign_in(code=code)
    except Exception as e:
        logging.error(e)
        flash("Something went wrong. Please try again.", category="danger")
        return redirect("/")
    flash("You are now signed in with Google.", category="success")
    return render_template(template_name_or_list="success.html", data=user_data, provider="google")


# --------------------------------------------------------------------------------
# ######  Sign in with Github Route
# --------------------------------------------------------------------------------
@app.route(rule="/login/github")
def sign_in_with_github() -> str:
    code = request.args.get(key="code")

    try:
        github_auth = GithubSocialAuth(
            client_id=os.environ["GITHUB_CLIENT_ID"],
            client_secret=os.environ["GITHUB_CLIENT_SECRET"],
        )
        user_data = github_auth.sign_in(code=code)
    except Exception as e:
        logging.error(e)
        flash("Something went wrong. Please try again.", category="danger")
        return redirect("/")
    flash("You are now signed in with Github.", category="success")
    return render_template(template_name_or_list="success.html", data=user_data, provider="github")


if __name__ == "__main__":
    app.run(debug=os.environ.get("DEBUG", False), host="localhost", port=5000)
