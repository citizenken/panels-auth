from flask import Flask, redirect, url_for, request, session
from flask_dance.contrib.google import make_google_blueprint, google
from oauth2client import client, GOOGLE_TOKEN_URI
import httplib2
import os

flask_secret = os.getenv('FLASK_SECRET', None)
client_id = os.getenv('CLIENT_ID', None)
client_secret = os.getenv('CLIENT_SECRET', None)

if not flask_secret:
    raise ValueError('FLASK_SECRET not set in environment')
if not client_id:
    raise ValueError('CLIENT_ID not set in environment')
if not client_secret:
    raise ValueError('CLIENT_SECRET not set in environment')

app = Flask(__name__)
app.secret_key = flask_secret

oauth_scopes = [
    'openid',
    'https://www.googleapis.com/auth/plus.me',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

blueprint = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    scope=oauth_scopes,
    reprompt_consent=True,
    offline=True
)

app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/")
def google_oauth():
    prompt = request.args.get('prompt', '')
    blueprint.authorization_url_params["prompt"] = prompt

    if not google.authorized:
        return redirect(url_for("google.login"))
    return redirect(url_for("electron_callback",
        id_token=google.token.get('id_token'),
        refresh_token=google.token.get('refresh_token')
        ))


@app.route("/callback")
def electron_callback():
    if not request.args.get('id_token'):
        return redirect(url_for('google_oauth'))
    return "authenticated"


@app.route("/refresh", methods=["GET"])
def refresh_access_token():
    refresh_token = request.args.get('refresh_token', '');
    credentials = client.OAuth2Credentials(
        None,
        client_id,
        client_secret,
        refresh_token,
        None,
        GOOGLE_TOKEN_URI,
        None)

    http = credentials.authorize(httplib2.Http())
    http = credentials.refresh(http)
    return credentials.id_token_jwt;


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return 'logged out'


if __name__ == "__main__":
    app.run()
