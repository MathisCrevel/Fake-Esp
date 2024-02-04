import flask
import sqlite3
import json
import datetime
import os

connection = sqlite3.connect('data.db')

cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS dogs (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, race TEXT)')
connection.commit()
connection.close()


app = flask.Flask(__name__, template_folder='views')

@app.route('/')
def home():
    return flask.render_template('index.html')