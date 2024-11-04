import requests
import json

def get_belib_data():
    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=belib-points-de-recharge-pour-vehicules-electriques-donnees-statiques"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['records']:

            for key in data['records'][0]['fields'].keys():
                print(f"- {key}")

            print("\nVérification des coordonnées:")
            for i, record in enumerate(data['records']):
                if 'geometry' in record and 'coordinates' in record['geometry']:
                    lon, lat = record['geometry']['coordinates']
                    print(f"Enregistrement {i}: Lat: {lat}, Lon: {lon}")
                else:
                    print(f"Enregistrement {i}: Coordonnées manquantes")

                # Afficher quelques champs supplémentaires pour plus d'informations
                fields = record['fields']
                for prise_type in ['prise_type_2', 'prise_type_3', 'prise_type_chademo', 'prise_type_combo_ccs', 'prise_type_ef']:
                    if fields.get(prise_type) == 'True':
                        print(f"    - {prise_type}")
                print()  # Ligne vide pour séparer les enregistrements

                # Limiter à 5 enregistrements pour l'exemple
                if i >= 4:
                    print("...")
                    break

        return data
    except requests.RequestException as e:
        print(f"Erreur lors de la requête à l'API: {e}")
        return None

# Appel de la fonction
if __name__ == "__main__":
    belib_data = get_belib_data()
    if belib_data:
        print("Données récupérées avec succès.")
    else:
        print("Échec de la récupération des données.")