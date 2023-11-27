import json
import geojson, geopandas, pandas as pd
import folium
from os import path
import random
from get_data import get_data
import asyncio

async def main():
    try:
        accident = geopandas.read_file("data/LightAccidents.geojson")
    except:
        print("Le fichier léger n'existe pas, exécution de la commande get_data.py...")
        await get_data()
        accident = geopandas.read_file("data/LightAccidents.geojson")

    # Liste des noms des 36 communes des Hauts-de-Seine
    communes_hauts_de_seine = [
        "Antony", "Asnières-sur-Seine", "Bagneux", "Bois-Colombes",
        "Boulogne-Billancourt", "Bourg-la-Reine", "Châtenay-Malabry", "Châtillon",
        "Clamart", "Clichy", "Colombes", "Courbevoie", "Fontenay-aux-Roses",
        "Garches", "La Garenne-Colombes", "Gennevilliers", "Issy-les-Moulineaux",
        "Levallois-Perret", "Malakoff", "Marnes-la-Coquette", "Meudon", "Montrouge",
        "Nanterre", "Neuilly-sur-Seine", "Puteaux", "Rueil-Malmaison", "Saint-Cloud",
        "Sceaux", "Sèvres", "Suresnes", "Vanves", "Vaucresson", "Ville-d'Avray", "Villeneuve-la-Garenne"
    ]

    # Générez des couleurs aléatoires pour chaque commune
    couleurs_acceptees = {'green', 'darkgreen', 'darkblue', 'gray', 'darkpurple', 'purple', 'lightgreen', 'red', 'lightblue', 'orange', 'black', 'cadetblue', 'pink', 'lightred', 'lightgray', 'beige', 'blue', 'darkred'}
    couleurs_par_commune = {commune: random.choice(list(couleurs_acceptees)) for commune in communes_hauts_de_seine}

    accident['date'] = pd.to_datetime(accident['date'])

    accidentYear = accident[accident['date'].dt.year == 2019]
    accidentYearMonth = accidentYear[accidentYear['date'].dt.month == 4]

    center_lat = accidentYearMonth['geometry'].apply(lambda geom: geom.y).mean()
    center_lon = accidentYearMonth['geometry'].apply(lambda geom: geom.x).mean()

    # Créez une carte de France avec folium.
    # print("Création de la carte...")
    m = folium.Map(location=[center_lat,center_lon], zoom_start=11)

    for index, row in accidentYearMonth.iterrows():
        popup_content = f"Date: {row['date']}<br>Heure: {row['heure']}"
        color = couleurs_par_commune.get(row['commune'], 'blue')
        folium.Marker(location=[row['geometry'].y, row['geometry'].x], popup=popup_content, parse_html=True, icon=folium.Icon(color=color)).add_to(m)

    # Sauvegardez la carte dans un fichier HTML.
    # print("Sauvegarde de la carte...")
    m.save('map.html')
    # print("Terminé !")

if __name__ == "__main__":
    asyncio.run(main())
