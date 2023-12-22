from concurrent.futures import ThreadPoolExecutor
import geopandas
from os import path, makedirs
import urllib.request
import asyncio
import ssl
from scraping import get_scraping_data

# Pour éviter les erreurs de certificat sur le réseau de l'ESIEE
ssl._create_default_https_context = ssl._create_unverified_context

# Fonction pour récupérer les données des accidents, des radars, des communes et des auto écoles
async def get_data() -> None:
    makedirs("data/", exist_ok=True)

    with ThreadPoolExecutor(max_workers=3) as executor:
        if not path.exists("data/big_accidents.geojson"):
            executor.submit(get_data_from_internet, "https://www.data.gouv.fr/fr/datasets/r/19b9f9d1-e24b-47f5-b908-e287339173b3", "data/big_accidents.geojson", "big_accidents", True)
        else:
            print("Le fichier big_accidents existe déjà !")

        if not path.exists("data/communes-92-hauts-de-seine.geojson"):
            executor.submit(get_data_from_internet, "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements/92-hauts-de-seine/communes-92-hauts-de-seine.geojson", "data/communes-92-hauts-de-seine.geojson", "communes-92-hauts-de-seine", False)
        else:
            print("Le fichier communes-92-hauts-de-seine existe déjà !")

        if not path.exists("data/driving_schools.geojson"):
            executor.submit(get_scraping_data)
        else:
            print("Le fichier driving_schools existe déjà !")

        if not path.exists("data/radars.csv"):
            executor.submit(get_data_from_internet, "https://www.data.gouv.fr/fr/datasets/r/8a22b5a8-4b65-41be-891a-7c0aead4ba51", "data/radars.csv", "radars", False)
        else:
            print("Le fichier radars existe déjà !")

# Fonction pour alléger le fichier big_accidents
def lighten_data():
    print("Lecture du fichier big_accidents (Cela peut prendre quelques temps, fichiers lourds)...")
    accident = geopandas.read_file("data/big_accidents.geojson")

    print("Création du fichier léger de big_accidents...")
    new_columns = ['date', 'heure', 'commune', 'geometry', 'code_insee', 'type_colli', 'type_acci', 'luminosite', 'adresse']
    accident = accident[new_columns]
    accident.to_file("data/light_accidents.geojson", driver='GeoJSON')
    print("big_accidents allégé !")

# Fonction pour récupérer les données depuis internet
def get_data_from_internet(url: str, path: str, filename: str, lourd: bool) -> None:
    if (lourd):
        print(f"Début du téléchargement de {filename} (Cela peut prendre quelques temps, fichiers lourds)...")
    else:
        print(f"Début du téléchargement de {filename} (fichier léger)...")
    urllib.request.urlretrieve(url, path)
    print(f"Fin du téléchargement de {filename}!")
    if (lourd):
        lighten_data()

if __name__ == "__main__":
    asyncio.run(get_data())

