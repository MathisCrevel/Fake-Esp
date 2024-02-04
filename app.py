import flask
import sqlite3

app = flask.Flask(__name__, template_folder='views')

connection = sqlite3.connect('data.db')

cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS dogs (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, race TEXT)')
connection.commit()
connection.close()


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


# Faire un form pour add
@app.route('/add', methods=['GET', 'POST'])
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

@app.route('/delete/<id>')
def delete(id):
   connection = sqlite3.connect('data.db')

   cursor = connection.cursor()
   cursor.execute('DELETE FROM dogs WHERE id = ' + id)
   connection.commit()
   connection.close()

   return flask.redirect('/')


@app.route('/api/dogs', methods=['GET'])
def get_dogs():
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

   return flask.jsonify(list_dogs)

@app.route('/api/dogs', methods=['POST'])
def add_dog():
   if flask.request.method == 'POST':
      # get data from request body
      name = flask.request.json['name']
      age = flask.request.json['age']
      race = flask.request.json['race']


      connection = sqlite3.connect('data.db')

      cursor = connection.cursor()
      cursor.execute('INSERT INTO dogs (name, age, race) VALUES ("' + name + '", "' + str(age) + '", "' + race + '")')
      connection.commit()
      connection.close()

      return flask.jsonify({
         "message": "Dog added successfully"
      })
# CRM (Postman) qui communique depuis l'extérieur en API REST via JSON sur le serveur Flask pour add et lister des chiens/clients
# le même serveur Flask affiche et add des données en MVC via les templates/views avec données dynamiques