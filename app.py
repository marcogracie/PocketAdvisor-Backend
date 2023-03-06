from flask import Flask
from flask import request
from flask import render_template
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from decouple import config
import requests
import json

app = Flask(__name__)
cred = credentials.Certificate('/Users/marcogracie/Documents/Personal/Code/StockMarketApp/PocketAdvisor-Backend/pocket-advisor-d79c2-firebase-adminsdk-23bkk-d0397417ea.json')

application = firebase_admin.initialize_app(cred)

db = firestore.client()

client_code = "c2dc99c563f2b980bdb3895065b25c38"
client_secret = config('secret_key', default='')

@app.route("/main", methods=['GET', 'POST'])
def main_page():
    if request.method == "GET":
        return render_template("/Users/marcogracie/Documents/Personal/Code/StockMarketApp/PocketAdvisor-Backend/signup.html")
    if request.method == "POST":
        # this is where we submit to database
        code = request.args.get('code')
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        head = {"Content-Type" : "application/x-www-form-urlencoded"}
        data = {"grant_type": "authorization_code", "code" : code, "client_id": client_code, "client_secret": client_secret, "redirect_uri": "http://127.0.0.1:5000/main"}
        access_data = requests.post("https://api.alpaca.markets/oauth/token", data = data, headers = head)
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

        # db.child("tokens").child(access_token).set(userData)
        db.collection('tokens').document(access_token).set(userData)
        return "Signup Finished. Please navigate back to the app and login!"
    