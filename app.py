from flask import Flask
import sqlite3
import json



app = Flask(__name__, template_folder='views', static_url_path='', static_folder='static')

@app.route("/")
def home():
    return "Hello, Flask!"