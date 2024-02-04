import flask
import sqlite3

app = flask.Flask(__name__, template_folder='views')

@app.route('/')
def home():
       return flask.render_template('index.html')

@app.route('/add')
def add():
        if flask.request.method == 'POST':
            name = flask.request.values.get('name')
            age = flask.request.values.get('age')
            race = flask.request.values.get('race')

            connection = sqlite3.connect('data.db')

            cursor = connection.cursor()
            cursor.execute('INSERT INTO dogs (name, age, race) VALUES ("' + name + '", "' + age + '", "' + race + '")')
            connection.commit()
            connection.close()

            return flask.redirect('/')
        else:
            return flask.render_template('add.html')