from flask import Flask
from flask import request
from flask import render_template
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from decouple import config
import requests
import json
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
cred = credentials.Certificate('/Users/marcogracie/Documents/Personal/Code/StockMarketApp/PocketAdvisor-Backend/pocket-advisor-d79c2-firebase-adminsdk-23bkk-d0397417ea.json')

application = firebase_admin.initialize_app(cred)

db = firestore.client()

client_code = "c2dc99c563f2b980bdb3895065b25c38"
client_secret = config('secret_key', default='')


@app.route('/main', methods=['GET', 'POST'])
def main_page():
    code = ""
    if request.method == "GET":
        code = request.args.get('code')
        app.logger.info(code)
        return render_template("signup.html")
    if request.method == "POST":
        # this is where we submit to database
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        head = {"Content-Type" : "application/x-www-form-urlencoded"}
        data = {"grant_type": "authorization_code", "code" : code, "client_id": client_code, "client_secret": client_secret, "redirect_uri": "http://127.0.0.1:5000/main"}
        access_data = requests.post("https://api.alpaca.markets/oauth/token", data = data, headers = head)
        app.logger.info(access_data)
        access_token = json.loads(access_data.text)["access_token"]
        head = {"Authorization": "Bearer " + access_token}
        polygon_data = json.loads(requests.get("https://api.alpaca.markets/oauth/token", headers=head).text)
        userData = {
            "name": name,
            "username": username,
            "password": password,
            "token": access_token,
            "polygonToken": polygon_data["id"]
        }

        db.collection('tokens').document(access_token).set(userData)
        return "Signup Finished. Please navigate back to the app and login!"
    