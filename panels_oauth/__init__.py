from flask import Flask, redirect, url_for, request, session
from flask_dance.contrib.google import make_google_blueprint, google
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
    prompt="select_account"
)

app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/")
def google_oauth():
    if not google.authorized:
        return redirect(url_for("google.login"))
    return redirect(url_for("electron_callback",
                    id_token=google.token.get('id_token')))


@app.route("/callback")
def electron_callback():
    if not request.args.get('id_token'):
        return redirect(url_for('google_oauth'))
    return "authenticated"


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return 'logged out'


if __name__ == "__main__":
    app.run()
