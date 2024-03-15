import sqlite3

#Établir une connexion à la base de données
#et créer un objet de connexion
connection = sqlite3.connect('Fake_StationMeteo.db')

#Créer un curseur vers la base de données
cursor = connection.cursor()

print("Ouverture de la base de données")
#Création de la table "Fake_Sonde"
cursor.execute ("""
                CREATE TABLE IF NOT EXISTS Fake_Sonde(
                id_Sonde INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name_sonde TEXT NOT NULL)
                ;
""")

connection.commit()

#Création de la table "Fake_Relevé"
cursor.execute ("""CREATE TABLE IF NOT EXISTS Fake_Releve(
                id_Fake_releve INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                Fake_temp FLOAT NOT NULL,
                Fake_humidite FLOAT NOT NULL,
                Fake_pression FLOAT NOT NULL,
                id_Sonde INTEGER NOT NULL, 
                FOREIGN KEY(id_Sonde) REFERENCES Fake_Sonde(id_Sonde)
                );
""")

connection.commit()
cursor.execute("""INSERT INTO Fake_Releve(Fake_temp, Fake_humidite, Fake_pression) values(22, 2, 2)""")
connection.commit()
#Supression de la ligne qui a pour pour resultat "2" dans la colonne "id_Sonde" dans la table "Sonde"  
"""cursor.execute (""""""DELETE FROM Sonde WHERE id_Sonde = 2"""""")

connection.commit()"""

connection.close()

