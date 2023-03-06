from flask import Flask
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)
cred = credentials.Certificate('/Users/marcogracie/Documents/Personal/Code/StockMarketApp/PocketAdvisor-Backend')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route("/main", methods=['GET', 'POST'])
def index():
    