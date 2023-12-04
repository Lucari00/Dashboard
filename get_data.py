import geopandas
from os import path, makedirs
import urllib.request
import asyncio
import ssl
from scraping import get_scraping_data

# Pour éviter les erreurs de certificat sur le réseau de l'ESIEE
ssl._create_default_https_context = ssl._create_unverified_context

async def get_data():
    if (not path.exists("data/")):
        makedirs("data/")

    if (not path.exists("data/BigAccidents.geojson")):
        await get_data_from_internet("https://www.data.gouv.fr/fr/datasets/r/19b9f9d1-e24b-47f5-b908-e287339173b3", "data/BigAccidents.geojson")
    else:
        print("Le fichier BigAccidents existe déjà !")
        
    if (not path.exists("data/LightAccidents.geojson")):
        lighten_data()
    else:
        print("Le fichier LightAccidents existe déjà !")

    if (not path.exists("data/communes-92-hauts-de-seine.geojson")):
        await get_data_from_internet("https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements/92-hauts-de-seine/communes-92-hauts-de-seine.geojson", "data/communes-92-hauts-de-seine.geojson")
    else:
        print("Le fichier communes-92-hauts-de-seine existe déjà !")

    await get_scraping_data(schools_number=30, regenerate=False)

def lighten_data():
    print("Lecture du fichier (Cela peut prendre quelques temps, fichiers lourds)...")
    accident = geopandas.read_file("data/BigAccidents.geojson")

    # créer le fichier léger
    print("Création du fichier léger...")
    new_columns = ['date', 'heure', 'commune', 'geometry', 'code_insee', 'type_colli']
    accident = accident[new_columns]
    accident.to_file("data/LightAccidents.geojson", driver='GeoJSON')
    print("Terminé !")

async def get_data_from_internet(url, filename):
    print("Début du téléchargement (Cela peut prendre quelques temps, fichiers lourds)...")
    urllib.request.urlretrieve(url, filename)
    print("Fin du téléchargement !")

if __name__ == "__main__":
    asyncio.run(get_data())

