import flask
import sqlite3
from random import randint
import json
from flask import request 

app = flask.Flask(__name__, template_folder='views')

connection = sqlite3.connect('Fake_StationMeteo.db')

cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Fake_Sonde(
               id_FakeSonde INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
               name_Sonde TEXT NOT NULL);"""
               )



cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Fake_Releve( 
               id_FakeReleve INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
               Fake_temp FLOAT,
               Fake_humidite FLOAT,
               Fake_pression FLOAT,
               id_FakeSonde INTEGER NOT NULL,
               FOREIGN KEY(id_FakeSonde) REFERENCES Fake_Sonde(id_FakeSonde));"""
               )
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

@app.route('/add/sonde', methods=['GET', 'POST'])
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

@app.route('/add/releve', methods=['GET', 'POST'])
def add_releve():
   if flask.request.method == 'POST':

      connection = sqlite3.connect('Fake_StationMeteo.db')

      nb_releves = flask.request.values.get('releve')
      id_Sonde = flask.request.values.get('sonde')
      nb_releves = int(nb_releves)
      print(type(nb_releves))

      for i in range(nb_releves):
         temp = randint(-10, 50)
         humidite = randint(0, 100)
         pression = randint(1000, 1050)

         cursor = connection.cursor()
         cursor.execute('SELECT id_FakeSonde FROM Fake_Sonde WHERE id_FakeSonde = ' + id_Sonde)
         reponse = cursor.fetchall()
         if reponse: 
            cursor.execute('INSERT INTO Fake_Releve (Fake_temp, Fake_humidite, Fake_pression, id_FakeSonde) VALUES (?,?,?,?)',(temp, humidite, pression, id_Sonde))
            connection.commit()
      connection.close()

      return flask.redirect('/')
   else:
      return flask.render_template('releve.html')

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
   cursor.execute('DELETE FROM Fake_Releve WHERE id_FakeSonde = ' + id)
   connection.commit()
   connection.close()

   return flask.redirect('/')


@app.route('/writedata', methods=['POST'])
def write_data():
    connection = sqlite3.connect('Fake_StationMeteo.db')
    cursor = connection.cursor()
    data = request.get_json()
    print("Received JSON data:")
    with open('releve.json', 'w') as json_file :
      json.dump(data, json_file)
    with open('releve.json', 'r') as json_file:
      data = json.load(json_file)
      print(data)
      cursor.execute('SELECT id_FakeSonde FROM Fake_Sonde WHERE id_FakeSonde = ' + str(data ['value']['id']))
      reponse = cursor.fetchall()
      if reponse: 
         cursor.execute('INSERT INTO Fake_Releve (Fake_temp, Fake_humidite, Fake_pression, id_FakeSonde) VALUES (?, ?, ?, ?)', (data['value']['temp'], data['value']['humidite'], data['value']['pression'], data ['value']['id']))
      else :
         print('La sonde '+ str(id) + 'n hexiste pas !')
         #cursor.execute('INSERT INTO Fake_Releve (Fake_temp, Fake_humidite, Fake_pression) VALUES (?, ?, ?)', (releve['value'][0], releve['value'][0], releve['value'][0]))

    connection.commit()
    connection.close()
        # Write data to file
    return "JSON data received successfully"
