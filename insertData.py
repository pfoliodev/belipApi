from data.api_client import get_belib_data
from database.db_manager import DatabaseManager


def main():
    data = get_belib_data()

    if not data or 'records' not in data:
        print("Aucune donnée n'a été récupérée ou le format des données est incorrect.")
        return

    with DatabaseManager() as db_manager:
        db_manager.create_tables()

        stations_count = 0
        bornes_count = 0

        for record in data['records']:
            # Insérer la station
            station_id = db_manager.insert_station(record)
            if station_id:
                stations_count += 1

                # Traiter les bornes
                fields = record['fields']
                prise_types = [
                    ('prise_type_2', 'Type 2'),
                    ('prise_type_3', 'Type 3'),
                    ('prise_type_chademo', 'CHAdeMO'),
                    ('prise_type_combo_ccs', 'Combo CCS'),
                    ('prise_type_ef', 'EF'),
                    ('prise_type_autre', 'Autre')
                ]

                for field, prise_type in prise_types:
                    if fields.get(field) == 'True':
                        borne_data = {
                            'type': prise_type,
                            'puissance': fields.get('puissance_nominale', 0)
                        }
                        db_manager.insert_borne(station_id, borne_data)
                        bornes_count += 1

        print(f"Nombre de stations insérées : {stations_count}")
        print(f"Nombre de bornes insérées : {bornes_count}")

        # Vérification finale dans la base de données
        db_manager.cursor.execute("SELECT COUNT(*) FROM stations")
        db_stations_count = db_manager.cursor.fetchone()[0]
        db_manager.cursor.execute("SELECT COUNT(*) FROM bornes")
        db_bornes_count = db_manager.cursor.fetchone()[0]

        print(f"Nombre de stations dans la base de données : {db_stations_count}")
        print(f"Nombre de bornes dans la base de données : {db_bornes_count}")


if __name__ == "__main__":
    main()