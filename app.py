#
# This is a simple Flask application that demonstrates how to use the OAuth2 PKCE flow for dental space one application
# You will need to install the following packages:
#
#   pip install flask requests pkce

# Run the application with:
#
#   flask run --port 4000  # please access the http://127.0.0.1:4000/ in your browser
#  
# http://localhost:4000/ will not work because it's not added to valid redirect_uris for the application
import os
import pkce
import requests
from flask import Flask, url_for, session, request
from flask import render_template, redirect


app = Flask(__name__)
app.secret_key = "!secret!"


OAUTH2_SERVER = os.environ.get('OAUTH2_SERVER')
OAUTH2_CLIENT_ID = os.environ.get('OAUTH2_CLIENT_ID')
OAUTH2_CLIENT_SECRET = os.environ.get('OAUTH2_CLIENT_SECRET')


code_verifier, code_challenge = pkce.generate_pkce_pair()


@app.route('/')
def homepage():
    user = session.get('user')
    return render_template('home.html', user=user)


@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    endpoint = f"{OAUTH2_SERVER}/oauth2/authorize/?response_type=code&client_id={OAUTH2_CLIENT_ID}&redirect_uri={redirect_uri}&scope=read_orders%20write_orders&code_challenge={code_challenge}&code_challenge_method=S256&state=1234"
    return redirect(endpoint)


@app.route('/auth')
def auth():
    redirect_uri = url_for('auth', _external=True)
    code = request.args.get('code')
    r = requests.post(f"{OAUTH2_SERVER}/oauth2/token/", data={
        "grant_type": "authorization_code",
        "code": code,
        "client_id": OAUTH2_CLIENT_ID,
        "client_secret": OAUTH2_CLIENT_SECRET,
        "code_verifier": code_verifier,
        "redirect_uri": redirect_uri
    })
    session['user'] = r.json()
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')