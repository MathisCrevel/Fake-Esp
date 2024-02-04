import flask
import sqlite3
import json
import datetime
import os



app = flask.Flask(__name__, template_folder='views')

@app.route('/')
def home():
    return flask.render_template('index.html')