import flask
import sqlite3

app = flask.Flask(__name__, template_folder='views')

@app.route('/')
def home():
   connection = sqlite3.connect('data.db')
   cursor = connection.cursor()
   cursor.execute('SELECT * FROM dogs')
   dogs = cursor.fetchall()
   connection.close()

   list_dogs = []

   for dog in dogs:
      list_dogs.append({
         "id": dog[0],
         "name": dog[1],
         "age": dog[2],
         "race": dog[3],
      }) 

   return flask.render_template('index.html', dogs=list_dogs)

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