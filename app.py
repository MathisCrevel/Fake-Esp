from flask import Flask
import sqlite3
import json
import datetime
import os




app = Flask(__name__, template_folder='views', static_url_path='', static_folder='static')

def read_file():
    with open('data.json', 'r') as fichier:
        data = fichier.read()
    return data

def write():
    data=json.loads(read_file())
    connection = sqlite3.connect('Station_meteof.db')
    cursor = connection.cursor()
    date_releve=datetime.datetime.now().strftime("%H:%M:%S")

    Fake_temp=round(data["data"][0]["temperature"],2)
    Fake_humidite=round(data["data"][1]["humidity"],2)
    Fake_pression=round(data["data"][2]["pressure"],2)
    cursor.execute("""select name_Sonde from Fake_Sonde where id_Sonde=1;""")
    data=cursor.fetchall()
    if data[0][0] == 1:
        cursor.execute("""INSERT INTO Fake_Releve(
                    date_releve,
                    Fake_temp,
                    Fake_humidite,
                    Fake_pression,
                    id_Sonde
                    ) 
                    VALUES (?,?,?,?,?);""",(date_releve,Fake_temp,Fake_humidite,Fake_pression,1))
    connection.commit()
    connection.close()

@app.route('/', methods=['GET'])
def home():
    write()
    connection=sqlite3.connect('Station_meteo.db')
    cursor=connection.cursor()
    cursor.execute("""SELECT moy_temp,moy_humidite,moy_pression FROM Releve ORDER BY id_Releve DESC LIMIT 1;""")
    data=cursor.fetchall()
    connection.commit()
    connection.close()