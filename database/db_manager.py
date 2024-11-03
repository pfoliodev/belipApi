import mysql.connector
from mysql.connector import Error
from config.database import DB_CONFIG

class DatabaseManager:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Connecté à la base de données MySQL")
        except Error as e:
            print(f"Erreur lors de la connexion à MySQL: {e}")
            raise

    def create_tables(self):
        try:
            # Création de la table stations
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nom VARCHAR(255),
                adresse VARCHAR(255),
                code_postal VARCHAR(10),
                latitude FLOAT,
                longitude FLOAT
            )
            """)

            # Création de la table bornes
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bornes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                station_id INT,
                puissance FLOAT,
                type_prise VARCHAR(50),
                FOREIGN KEY (station_id) REFERENCES stations(id)
            )
            """)

            self.connection.commit()
            print("Tables créées avec succès")
        except Error as e:
            print(f"Erreur lors de la création des tables: {e}")
            self.connection.rollback()

    def insert_station(self, station_data):
        try:
            query = """
            INSERT INTO stations (nom, adresse, code_postal, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s)
            """
            if 'geometry' in station_data and 'coordinates' in station_data['geometry']:
                lon, lat = station_data['geometry']['coordinates']
            else:
                lat = station_data['fields'].get('lat') or station_data['fields'].get('latitude')
                lon = station_data['fields'].get('lon') or station_data['fields'].get('longitude')

            if lat is None or lon is None:
                print(f"Coordonnées manquantes pour la station: {station_data['fields'].get('nom_station')}")
                lat = 0.0
                lon = 0.0

            values = (
                station_data['fields'].get('nom_station'),
                station_data['fields'].get('adresse_station'),
                station_data['fields'].get('code_postal_station'),
                float(lat),
                float(lon)
            )
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f"Erreur lors de l'insertion de la station: {e}")
            self.connection.rollback()
            return None

    def insert_borne(self, station_id, borne_data):
        try:
            query = """
            INSERT INTO bornes (station_id, type_prise, puissance)
            VALUES (%s, %s, %s)
            """
            values = (
                station_id,
                borne_data['type'],
                float(borne_data['puissance'])
            )
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Erreur lors de l'insertion de la borne: {err}")
            self.connection.rollback()
            return None

    def get_station_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM stations")
        return self.cursor.fetchone()[0]

    def get_borne_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM bornes")
        return self.cursor.fetchone()[0]

    def get_all_stations(self):
        try:
            query = "SELECT id, nom, adresse, latitude, longitude FROM stations"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Erreur lors de la récupération des stations: {err}")
            return []

    def get_stations_geojson(self):
        try:
            query = "SELECT id, nom, adresse, latitude, longitude FROM stations"
            self.cursor.execute(query)
            stations = self.cursor.fetchall()

            features = []
            for station in stations:
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [station[4], station[3]]  # [longitude, latitude]
                    },
                    "properties": {
                        "id": station[0],
                        "nom": station[1],
                        "adresse": station[2]
                    }
                }
                features.append(feature)

            return {
                "type": "FeatureCollection",
                "features": features
            }
        except mysql.connector.Error as err:
            print(f"Erreur lors de la récupération des stations: {err}")
            return None

    def close(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Connexion à la base de données fermée")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()