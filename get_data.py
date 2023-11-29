import geopandas
from os import path, makedirs
import urllib.request
import asyncio
import ssl

# Pour éviter les erreurs de certificat sur le réseau de l'ESIEE
ssl._create_default_https_context = ssl._create_unverified_context

async def get_data():
    if (not path.exists("data/")):
        makedirs("data/")

    if (not path.exists("data/BigAccidents.geojson")):
        await get_data_from_internet("https://www.data.gouv.fr/fr/datasets/r/5c4f3f0f-1a6c-4f6f-9b2e-9a2a6b0b9e2f", "data/BigAccidents.geojson")
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

