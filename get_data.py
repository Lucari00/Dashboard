import geopandas
from os import path
import urllib.request

async def get_data():
    if (not path.exists("data/LightAccidents.geojson")):
        #télécharger le fichier
        get_data_from_internet("https://www.data.gouv.fr/fr/datasets/r/19b9f9d1-e24b-47f5-b908-e287339173b3", "data/BigAccidents.geojson")
        print("Lecture du fichier...")
        accident = geopandas.read_file("data/BigAccidents.geojson")

        # créer le fichier léger
        print("Création du fichier léger...")
        new_columns = ['date', 'heure', 'commune', 'geometry']
        accident = accident[new_columns]
        accident.to_file("data/LightAccidents.geojson", driver='GeoJSON')
    else:
        print("Le fichier léger existe déjà !")
        # print("Lecture du fichier léger...")
        # accident = geopandas.read_file("data/LightAccidents.geojson")

def get_data_from_internet(url, filename):
    print("Début du téléchargement...")
    urllib.request.urlretrieve(url, filename)
    print("Fin du téléchargement !")

if __name__ == "__main__":
    get_data()

