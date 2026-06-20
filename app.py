from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Cloud Expense Tracker is Running!"