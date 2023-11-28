import json
import geojson, geopandas, pandas as pd
import folium
from os import path
import random
from get_data import get_data
import asyncio
from dash import Dash, dcc, html, Input, Output, callback
import calendar
import plotly.graph_objects as go

app = Dash(__name__)

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


async def main():
    try:
        accident = geopandas.read_file("data/LightAccidents.geojson")
    except:
        print("Le fichier léger n'existe pas, exécution de la commande get_data.py...")
        await get_data()
        accident = geopandas.read_file("data/LightAccidents.geojson")
    
    # print("Création de la carte...")
    base_month = 4
    base_year = 2019

    # m = create_map(accident, base_year, base_month)

    accident['date'] = pd.to_datetime(accident['date'])

    accident_base_year = accident[accident['date'].dt.year == base_year]
    accident_base_year_month = accident_base_year[accident_base_year['date'].dt.month == base_month]

    app.layout = html.Div(children=[

        html.H1(id="title-dash", children='Carte des accidents de la route dans les Hauts-de-Seine en avril 2019',
                style={'textAlign': 'center', 'color': "#503D36"}),
        html.Div(id="title-map", children='''Cette carte représente les accidents de la route dans les Hauts-de-Seine en avril 2019.''',
                style={'textAlign': 'center', 'color': "#503D36"}),
        html.Div(children=[html.Iframe(id='map', srcDoc=None, width='100%', height='500', style={'overflow': 'hidden'})], style={'overflow': 'hidden'}),
        html.Div(id='text-number-accident', style={'textAlign': 'center', 'color': "#503D36"}),

        html.Div(id="container-change-date", 
            children=['''Choisissez une année et un mois pour afficher les accidents de la route.''',
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id='month-dropdown',
                            options=[
                                {'label': month, 'value': pd.to_datetime(month, format='%B').month} for month in sorted(accident['date'].dt.month_name().unique(), key=lambda x: pd.to_datetime(x, format='%B').month)
                            ],
                            value=4,  # Valeur par défaut
                            style={'width': '100px'},
                            clearable=False
                        ),

                        dcc.Dropdown(
                            id='year-dropdown',
                            options=[
                                {'label': str(year), 'value': year} for year in sorted(accident['date'].dt.year.unique())
                            ],
                            value=2019,  # Valeur par défaut
                            style={'width': '100px'},
                            clearable=False
                        ),
                    ], 
                    style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center'}
                ),
            ], 
            style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'justify-content': 'center', 'width': '100%'}
        ),

        dcc.Graph(
            id='histogramme-accident',
            figure={
                'data': [
                    go.Bar(
                        x=sorted(accident['date'].dt.month_name().unique(), key=lambda x: pd.to_datetime(x, format='%B').month),
                        y=accident_base_year_month.groupby(accident_base_year_month['date'].dt.month)['date'].count(),
                        name='Nombre d\'accidents',
                        marker=go.bar.Marker(
                            color='rgb(55, 83, 109)'
                        )
                    )
                ],
                'layout': go.Layout(
                    title='Nombre d\'accidents par mois',
                    xaxis={'title': 'Mois'},
                    yaxis={'title': 'Nombre d\'accidents'}
                )
            }
        ),

        html.Div(id="container-change-date-slider",
            children=[
                dcc.Slider(
                    id='year-slider',
                    min=accident['date'].dt.year.min(),
                    max=accident['date'].dt.year.max(),
                    value=base_year,
                    marks={str(year): str(year) for year in accident['date'].dt.year.unique()},
                    step=None
                ),
            ],
            
        )
    ])

@app.callback(
    Output(component_id='histogramme-accident', component_property='figure'),
    Input(component_id='year-slider', component_property='value')
)
def update_histogramme(year):
    accident = geopandas.read_file("data/LightAccidents.geojson")

    accident['date'] = pd.to_datetime(accident['date'])
    accident_year = accident[accident['date'].dt.year == year]

    return {
        'data': [
            go.Bar(
                x=sorted(accident['date'].dt.month_name().unique(), key=lambda x: pd.to_datetime(x, format='%B').month),
                y=accident_year.groupby(accident_year['date'].dt.month)['date'].count(),
                name='Nombre d\'accidents',
                marker=go.bar.Marker(
                    color='rgb(55, 83, 109)'
                )
            )
        ],
        'layout': go.Layout(
            title=f'Nombre d\'accidents par mois en {year}',
            xaxis={'title': 'Mois'},
            yaxis={'title': 'Nombre d\'accidents'}
        )
    }

@app.callback(
    Output(component_id='map', component_property='srcDoc'),
    Output(component_id='text-number-accident', component_property='children'),
    Output(component_id='title-dash', component_property='children'),
    Output(component_id='title-map', component_property='children'),
    Input(component_id='year-dropdown', component_property='value'),
    Input(component_id='month-dropdown', component_property='value')
)
def update_map(year, month):
    accident = geopandas.read_file("data/LightAccidents.geojson")

    accident['date'] = pd.to_datetime(accident['date'])

    m = create_map(accident, year, month)

    accidentYear = accident[accident['date'].dt.year == year]
    accidentYearMonth = accidentYear[accidentYear['date'].dt.month == month]

    # récupérer le nom du mois en français
    month_name = calendar.month_name[month]

    return m, f'''Nombre d'accidents: {len(accidentYearMonth)}''', f'''Carte des accidents de la route dans les Hauts-de-Seine en {month_name} {year}''', f'''Cette carte représente les accidents de la route dans les Hauts-de-Seine en {month_name} {year}.'''

def create_map(data, year, month):
    accidentYear = data[data['date'].dt.year == year]
    accidentYearMonth = accidentYear[accidentYear['date'].dt.month == month]

    center_lat = accidentYearMonth['geometry'].apply(lambda geom: geom.y).mean()
    center_lon = accidentYearMonth['geometry'].apply(lambda geom: geom.x).mean()

    # Créez une carte de France avec folium.
    # print("Création de la carte...")
    m = folium.Map(location=[center_lat,center_lon], zoom_start=11)

    for index, row in accidentYearMonth.iterrows():
        popup_content = f"Date: {row['date'].date()}<br>Heure: {row['heure']}"
        color = couleurs_par_commune.get(row['commune'], 'blue')
        folium.Marker(location=[row['geometry'].y, row['geometry'].x], popup=popup_content, parse_html=True, icon=folium.Icon(color=color)).add_to(m)

    # Sauvegardez la carte dans un fichier HTML.
    # print("Sauvegarde de la carte...")
    return m._repr_html_()
    # print("Terminé !")

if __name__ == "__main__":
    asyncio.run(main())
    app.run_server(debug=True)
