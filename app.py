from flask import Flask
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from decouple import config

app = Flask(__name__)
cred = credentials.Certificate('/Users/marcogracie/Documents/Personal/Code/StockMarketApp/PocketAdvisor-Backend/pocket-advisor-d79c2-firebase-adminsdk-23bkk-d0397417ea.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

client_code = c2dc99c563f2b980bdb3895065b25c38
client_secret = config('secret_key', default='')

@app.route("/main", methods=['GET', 'POST'])
def main_page():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        # this is where we submit to database
        code = request.args.get('code')
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        head = {"Content-Type" : "application/x-www-form-urlencoded"}
        data = {"grant_type": "authorization_code", "code" : code, "client_id": client_code}

    