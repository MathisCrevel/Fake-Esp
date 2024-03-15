import flask
import sqlite3

app = flask.Flask(__name__, template_folder='views')

connection = sqlite3.connect('Fake_StationMeteo.db')

cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS Fake_Sonde (id_FakeSonde INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name_Sonde TEXT NOT NULL);')



cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS Fake_Releve (id_FakeReleve INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Fake_temp FLOAT , Fake_humidite FLOAT, Fake_pression FLOAT);')
connection.commit()
connection.close()

@app.route('/')
def home():
   connection = sqlite3.connect('Fake_StationMeteo.db')
   cursor = connection.cursor()
   cursor.execute('SELECT id_FakeReleve, Fake_temp, Fake_humidite, Fake_pression FROM Fake_Releve ORDER BY id_FakeReleve DESC LIMIT 1;')
   Fake_Releve = cursor.fetchall()
   cursor.execute('SELECT * FROM Fake_Sonde ORDER BY id_FakeSonde DESC LIMIT 1;')
   Fake_Sonde = cursor.fetchall()
   connection.close()

   list_releve = []

   for releve in Fake_Releve:
      list_releve.append({
         "id": releve[0],
         "temp": releve[1],
         "humidite": releve[2],
         "pression": releve[3],
      }) 

   list_sonde = []
   for sonde in Fake_Sonde:
      list_sonde.append({
      "id": sonde[0],
      "nom": sonde[1]
      })

   return flask.render_template('index.html', releve=list_releve, sonde=list_sonde)


# Faire un form pour add
@app.route('/add', methods=['GET', 'POST'])
def add():
   if flask.request.method == 'POST':
      name = flask.request.values.get('nom')
      
      connection = sqlite3.connect('Fake_StationMeteo.db')

      cursor = connection.cursor()
      cursor.execute('INSERT INTO Fake_Sonde (name_Sonde) VALUES (?)',(name,))
      connection.commit()
      connection.close()

      return flask.redirect('/')
   else:
      return flask.render_template('add.html')

@app.route('/delete_Releve/<id>')
def delete_Releve(id):
   connection = sqlite3.connect('Fake_StationMeteo.db')

   cursor = connection.cursor()
   cursor.execute('DELETE FROM Fake_Releve WHERE id_FakeReleve = ' + id)
   connection.commit()
   connection.close()

   return flask.redirect('/')

@app.route('/delete_Sonde/<id>')
def delete_Sonde(id):
   connection = sqlite3.connect('Fake_StationMeteo.db')

   cursor = connection.cursor()
   cursor.execute('DELETE FROM Fake_Sonde WHERE id_FakeSonde = ' + id)
   connection.commit()
   connection.close()

   return flask.redirect('/')

@app.route('/api/dogs', methods=['GET'])
def get_dogs():
   connection = sqlite3.connect('Fake_StationMeteo.db')
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


      connection = sqlite3.connect('Fake_StationMeteo.db')

      cursor = connection.cursor()
      cursor.execute('INSERT INTO dogs (name, age, race) VALUES ("' + name + '", "' + str(age) + '", "' + race + '")')
      connection.commit()
      connection.close()

      return flask.jsonify({
         "message": "Dog added successfully"
      })
# CRM (Postman) qui communique depuis l'extérieur en API REST via JSON sur le serveur Flask pour add et lister des chiens/clients
# le même serveur Flask affiche et add des données en MVC via les templates/views avec données dynamiques