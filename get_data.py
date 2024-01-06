"""
    Script pour récupérer les données des accidents
    radars, communes et auto écoles
"""
from os import path, makedirs
from concurrent.futures import ThreadPoolExecutor
import urllib.request
import asyncio
import ssl
import geopandas
from scraping import get_scraping_data

# Pour éviter les erreurs de certificat sur le réseau de l'ESIEE
# Source:
# https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
ssl._create_default_https_context = ssl._create_unverified_context

# Fonction pour récupérer les données des accidents, des radars, des communes et des auto écoles
async def get_data() -> None:
    """
        Procédure pour récupérer les données des accidents,
        radars, communes et auto écoles

        Returns:
            None
    """
    makedirs("data/", exist_ok=True)

    with ThreadPoolExecutor(max_workers=3) as executor:
        if not path.exists("data/big_accidents.geojson"):
            executor.submit(
                get_data_from_internet,
                "https://www.data.gouv.fr/fr/datasets/r/19b9f9d1-e24b-47f5-b908-e287339173b3",
                "data/big_accidents.geojson",
                "big_accidents",
                True)
        else:
            print("Le fichier big_accidents existe déjà !")

        if not path.exists("data/communes-92-hauts-de-seine.geojson"):
            executor.submit(
                get_data_from_internet,
                ("https://opendata.hauts-de-seine.fr/api/explore/v2.1/catalog/datasets/"
                "communes/exports/geojson?lang=fr&timezone=Europe/Berlin"),
                "data/communes-92-hauts-de-seine.geojson",
                "communes-92-hauts-de-seine",
                False)
        else:
            print("Le fichier communes-92-hauts-de-seine existe déjà !")

        if not path.exists("data/driving_schools.geojson"):
            executor.submit(get_scraping_data)
        else:
            print("Le fichier driving_schools existe déjà !")

        if not path.exists("data/radars.csv"):
            executor.submit(
                get_data_from_internet,
                "https://www.data.gouv.fr/fr/datasets/r/8a22b5a8-4b65-41be-891a-7c0aead4ba51",
                "data/radars.csv",
                "radars",
                False)
        else:
            print("Le fichier radars existe déjà !")

def lighten_data() -> None:
    """
        Procédure pour alléger le fichier big_accidents

        Returns:
            None
    """
    print("Lecture du fichier big_accidents (Cela peut prendre quelques temps, fichiers lourds)...")
    accident = geopandas.read_file("data/big_accidents.geojson")

    print("Création du fichier léger de big_accidents...")
    new_columns = [
        'date','heure', 'commune', 'geometry', 'code_insee',
        'type_colli', 'type_acci', 'luminosite', 'adresse'
    ]
    accident = accident[new_columns]
    accident.to_file("data/light_accidents.geojson", driver='GeoJSON')
    print("big_accidents allégé !")


def get_data_from_internet(url: str, filepath: str, filename: str, lourd: bool) -> None:
    """
        Procédure pour télécharger un fichier depuis internet
        Si le fichier est lourd, on allège le fichier

        Args:
            url (str): l'url du fichier à télécharger
            filepath (str): le chemin du fichier
            filename (str): le nom du fichier
            lourd (bool): si le fichier est lourd ou non

        Returns:
            None
    """
    if lourd:
        print(
            f"Début du téléchargement de {filename} "
            "Cela peut prendre quelques temps, fichiers lourds..."
        )
    else:
        print(f"Début du téléchargement de {filename} (fichier léger)...")
    urllib.request.urlretrieve(url, filepath)
    print(f"Fin du téléchargement de {filename}!")
    if lourd:
        lighten_data()

if __name__ == "__main__":
    asyncio.run(get_data())
