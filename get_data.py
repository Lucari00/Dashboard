import geopandas
from os import path, makedirs
import urllib.request
import asyncio

async def get_data():
    if (not path.exists("data/")):
        #télécharger le fichier
        makedirs("data/")
        
    if (not path.exists("data/LightAccidents.geojson")):
        await get_data_from_internet("https://www.data.gouv.fr/fr/datasets/r/19b9f9d1-e24b-47f5-b908-e287339173b3", "data/BigAccidents.geojson")
        lighten_data()
    else:
        print("Le fichier léger existe déjà !")

def lighten_data():
    print("Lecture du fichier (Cela peut prendre quelques temps, fichiers lourds)...")
    accident = geopandas.read_file("data/BigAccidents.geojson")

    # créer le fichier léger
    print("Création du fichier léger...")
    new_columns = ['date', 'heure', 'commune', 'geometry']
    accident = accident[new_columns]
    accident.to_file("data/LightAccidents.geojson", driver='GeoJSON')
    print("Terminé !")

async def get_data_from_internet(url, filename):
    print("Début du téléchargement (Cela peut prendre quelques temps, fichiers lourds)...")
    urllib.request.urlretrieve(url, filename)
    print("Fin du téléchargement !")

if __name__ == "__main__":
    asyncio.run(get_data())

