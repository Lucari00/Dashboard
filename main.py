import time
import geopandas, pandas as pd
import folium
import random
from get_data import get_data
import asyncio
from dash import Dash, dcc, html, Input, Output, State, callback
import calendar
import plotly.graph_objects as go
import plotly.express as px

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

# Couleur de fond
bg_color = '#FCF5ED'

async def main():
    global accident
    global geo_data_92
    global driving_schools
    global radars
    try:
        accident = geopandas.read_file("data/light_accidents.geojson")
        geo_data_92 = geopandas.read_file("data/communes-92-hauts-de-seine.geojson")
        driving_schools = geopandas.read_file("data/driving_schools.geojson")
        radars = pd.read_csv("data/radars.csv")
    except:
        print("Il manque au moins un fichier, exécution de la commande get_data.py")
        print("Pour récupérer les données, les fonctions fonctionnent sur différents threads, ce qui permet de gagner du temps.")
        print("")
        print("Dans de bonnes conditions, le temps d'exécution est d'environ 220 secondes sur les machines de l'ESIEE...")
        print("ATTENTION, MEME SI LE MESSAGE \"Scraping terminé !\" S'AFFICHE, CELA NE VEUT PAS DIRE QUE TOUT EST FINI !")
        print("IL EST TRES PROBABLE QUE L'OUVERTURE DU FICHIER LOURD PRENNE DU TEMPS !")
        print("")
        start = time.time()
        await get_data()
        print("")
        print(f"Temps d'exécution: {time.time() - start} secondes")
        print("Lectures des données...")

        accident = geopandas.read_file("data/light_accidents.geojson")
        geo_data_92 = geopandas.read_file("data/communes-92-hauts-de-seine.geojson")
        driving_schools = geopandas.read_file("data/driving_schools.geojson")
        radars = pd.read_csv("data/radars.csv")
        print("Création du dashboard...")
    
    base_year = 2019

    # Convertir la date, qui est en string, en datetime
    accident['date'] = pd.to_datetime(accident['date'])

    # Crée une carte choroplèthe, non dynamique
    choropleth_map = create_choropleth_map()

    # Crée un histogramme de la gravité des accidents par heure, non dynamique
    histogram_gravity = create_histogram_gravity_by_hour()

    # Le layout du dashboard
    app.layout = html.Div(children=[

        # Titre du dashboard
        html.H1(id="title-dash", children='Dashboard des accidents de la route dans les Hauts-de-Seine',
                style={'textAlign': 'center', 'color': "#503D36", 'font-size': '40px'}),
    
        # Titre de la carte des accidents en fonction du mois et de l'année
        html.H2(id="title-map", children='''Carte représentant les accidents de la route dans les Hauts-de-Seine en avril 2019.''',
                style={'textAlign': 'center', 'color': "#503D36", 'margin-bottom': '15px'}),
        
        # Contenant de la carte des accidents en fonction du mois et de l'année
        html.Div(children=[html.Iframe(id='map', srcDoc=None, width='80%', height='500px', style={'border': f'2px solid #FFA500'})], style={'height': '500px', 'width': '100%', 'margin-bottom': '15px', 'justify-content': 'center', 'align-items': 'center', 'display': 'flex'}),
        
        # Texte qui affiche le nombre d'accidents en fonction du mois et de l'année
        html.Div(id='text-number-accident', children=['''Nombre d'accidents pendant cette période : '''], style={'textAlign': 'center', 'color': "#503D36", 'margin-bottom': '15px'}),

        # Contenant du menu pour changer la
        html.Div(id="container-change-date", 
            children=['''Choisissez une année et un mois pour afficher les accidents de la route sur la carte.''',
                html.Div(
                    children=[
                        # Dropdown pour choisir le mois
                        dcc.Dropdown(
                            id='month-dropdown',
                            options=[
                                {'label': month, 'value': pd.to_datetime(month, format='%B').month} for month in sorted(accident['date'].dt.month_name().unique(), key=lambda x: pd.to_datetime(x, format='%B').month)
                            ],
                            value=4,  # Valeur par défaut
                            style={'width': '100px'},
                            clearable=False
                        ),

                        # Dropdown pour choisir l'année
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
            style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'justify-content': 'center', 'width': '100%', 'color': "#503D36", 'text-align': 'center'}
        ),

        # Grapique de l'histogramme des accidents par mois d'une année
        dcc.Graph(
            id='histogramme-accidents',
            figure={},
        ),

        # Courbe du nombre d'accidents par heure d'une journée d'une année
        dcc.Graph(
            id='graphique-accidents-heures',
            figure={},
        ),

        # Slider pour changer l'année des 2 graphiques précédents
        dcc.Slider(
            id='year-slider',
            min=accident['date'].dt.year.min(),
            max=accident['date'].dt.year.max(),
            value=base_year,
            marks={str(year): str(year) for year in accident['date'].dt.year.unique()},
            step=None,
        ),

        # Button pour arrêter le slider dynamique
        html.Div(
            children=[
                html.Button(
                    id='play-button', 
                    children='▶️', 
                    n_clicks=0, 
                    style={
                        'background-color': 'transparent',  # Button color
                        'color': 'white',  # Text color
                        'padding': '15px 32px',  # Top/bottom padding, left/right padding
                        'text-align': 'center',  # Center the text
                        'text-decoration': 'none',  # Remove underline
                        'display': 'inline-block',  
                        'font-size': '32px',  # Increase font size
                        'margin': '4px 2px',  # Add some margin
                        'border': 'none',  # Remove border
                        'cursor': 'pointer',  # Add a hand cursor on hover
                    }
                )
            ],
            style={'display': 'flex', 'justify-content': 'center'}
        ),

        # Histogramme de la gravité des accidents par heure de tous les accidents
        dcc.Graph(
            id='histogram-grave-hour',
            figure=histogram_gravity
        ),

        # Interval qui permet de rendre dynamique le slider et donc les graphiques
        dcc.Interval(id="interval", interval=1*3000, n_intervals=0, disabled=False),

        # Titre de la carte choroplèthe
        html.H2(id="title-map-choropleth", children='''Carte choroplèthe représentant le nombre d'accidents par commune.''',
                style={'textAlign': 'center', 'color': "#503D36"}),

        # Contenant de la carte choroplèthe
        html.Div(children=[html.Iframe(id='map-choropleth', srcDoc=choropleth_map, width='80%', height='500px', style={'border': f'2px solid #FFA500'})], style={'height': '500px', 'width': '100%', 'margin-bottom': '15px', 'justify-content': 'center', 'align-items': 'center', 'display': 'flex'}),
    
    ], style={'width': '100%', 'padding': '0', 'padding-bottom': '15px', 'font-family': 'Helvetica', 'background-color': bg_color})

# Fonction pour créer l'histogramme de la gravité des accidents par heure
def create_histogram_gravity_by_hour() -> go.Figure:
    accident_heure = accident.copy()

    accident_heure['heure'] = pd.to_datetime(accident['heure'], format='%H:%M:%S').dt.hour
    accident_sorted = accident_heure.sort_values(by='heure')

    accidents_mortels = accident_sorted[accident_sorted['type_acci'] == 'Mortel'].groupby('heure').size().reset_index(name='accidents')
    accidents_mortels['type_acci'] = 'Mortel'

    accidents_graves = accident_sorted[accident_sorted['type_acci'] == 'Grave'].groupby('heure').size().reset_index(name='accidents')
    accidents_graves['type_acci'] = 'Grave'

    accidents_legers = accident_sorted[accident_sorted['type_acci'] == 'Léger'].groupby('heure').size().reset_index(name='accidents')
    accidents_legers['type_acci'] = 'Léger'

    accident_sorted = pd.concat([accidents_mortels, accidents_graves, accidents_legers], ignore_index=True)

    # Pivoter la table pour avoir les catégories comme colonnes
    accident_sorted = accident_sorted.pivot(index='heure', columns='type_acci', values='accidents')

    # Calculer les pourcentages
    accident_sorted = accident_sorted.div(accident_sorted.sum(axis=1), axis=0) * 100

    # Remplacer les valeurs NaN par 0
    accident_sorted = accident_sorted.fillna(0)

    # Réinitialiser l'index
    accident_sorted.reset_index(inplace=True)

    accident_sorted = pd.melt(accident_sorted, id_vars='heure', var_name='type_acci', value_name='proportion')

    colors = {'Mortel': '#FF0000', 'Grave': '#FFA500', 'Léger': '#EEDD00'}

    fig = px.bar(accident_sorted, 
            x='heure', 
            y='proportion', 
            color='type_acci',
            color_discrete_map=colors,
            labels={'heure': 'Heure de l\'accident', 'proportion': 'Proportion d\'accidents', 'type_acci': 'Type d\'accident'},
            title='Proportion d\'accidents de chaque catégorie pour chaque heure de la journée de 2006 à 2021',
        )
    
    fig.update_layout(
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color 
    )

    return fig

# Callback pour gérer l'interval et le slider dynamique
@callback(
        Output('year-slider', 'value'),
        Input('interval', 'n_intervals'),
        State('year-slider', 'value')
    )
def on_tick(_, year):
    years = sorted(accident['date'].dt.year.unique())
    year_index = years.index(year)
    return years[year_index + 1 if year_index + 1 < len(years) else 0]

# Callback pour mettre à jour l'histogramme des accidents par mois
@app.callback(
    Output(component_id='histogramme-accidents', component_property='figure'),
    Input(component_id='year-slider', component_property='value')
)
def update_histogramme(year):
    accident_year = accident[accident['date'].dt.year == year]

    return {
        'data': [
            go.Bar(
                x=sorted(accident['date'].dt.month_name().unique(), key=lambda x: pd.to_datetime(x, format='%B').month),
                y=accident_year.groupby(accident_year['date'].dt.month)['date'].count(),
                name='Nombre d\'accidents',
                marker=go.bar.Marker(
                    color='#EEDD00'
                )
            )
        ],
        'layout': go.Layout(
            title=f'Nombre d\'accidents par mois en {year}',
            xaxis={'title': 'Mois'},
            yaxis={'title': 'Nombre d\'accidents'},
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color  
        )
    }

# Callback pour mettre à jour la courbe du nombre d'accidents par heure
@app.callback(
    Output(component_id='graphique-accidents-heures', component_property='figure'),
    Input(component_id='year-slider', component_property='value')
)
def update_graphique(year):
    accident_year = accident[accident['date'].dt.year == year]
    #trier par heure
    accident_year = accident_year.sort_values(by=['heure'])
    # nombre d'accidents par heure
    heure = [int(hour[0:2]) for hour in accident_year['heure'].to_list()]
    nombre_accident = []
    for hour in range(24):
        nombre_accident.append(heure.count(hour))
    heure = [hour for hour in range(24)]

    # graphique du nombre d'accidents en fonction de l'heure
    return {
        'data': [
            go.Scatter(x=heure, y=nombre_accident, mode='lines+markers', line=dict(color='#EEDD00'))
        ],
        'layout': go.Layout(
            title=f'Nombre d\'accidents par heure de la journée en {year}',
            xaxis={'title': 'Heure'},
            yaxis={'title': 'Nombre d\'accidents'},
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color  
        )
    }

# Callback pour gérer le bouton pour stopper le slider dynamique
@app.callback(
    Output('interval', 'disabled'),
    Output('play-button', 'children'),
    Input('play-button', 'n_clicks'),
)
def on_play_button_click(n_clicks):
    if n_clicks is None: return False, '⏸️'
    if n_clicks % 2 == 1:
        return True, '▶️'
    else:
        return False, '⏸️'

# Callback pour mettre à jour la carte des accidents en fonction du mois et de l'année
@app.callback(
    Output(component_id='map', component_property='srcDoc'),
    Output(component_id='text-number-accident', component_property='children'),
    Output(component_id='title-map', component_property='children'),
    Input(component_id='year-dropdown', component_property='value'),
    Input(component_id='month-dropdown', component_property='value')
)
def update_map(year, month):
    m = create_map(accident, year, month)

    accidentYear = accident[accident['date'].dt.year == year]
    accidentYearMonth = accidentYear[accidentYear['date'].dt.month == month]

    # récupérer le nom du mois en français
    month_name = calendar.month_name[month]

    return m, f'''Nombre d'accidents pendant cette période: {len(accidentYearMonth)}''', f'''Carte représentant les accidents de la route dans les Hauts-de-Seine en {month_name} {year}.'''

def create_map(data, year, month):
    accident_year = data[data['date'].dt.year == year]
    accident_year_month = accident_year[accident_year['date'].dt.month == month]

    center_lat = accident_year_month['geometry'].apply(lambda geom: geom.y).mean()
    center_lon = accident_year_month['geometry'].apply(lambda geom: geom.x).mean()
    m = folium.Map(location=[center_lat,center_lon], zoom_start=13)

    for index, row in accident_year_month.iterrows():
        popup_content = f"""<div style='white-space: pre-wrap; width: 200px;'>
<b>📍  Adresse</b> : {row['adresse']}<br>
<b>📅 Date</b> : {row['date'].date()}<br>
<b>🕐 Heure</b> : {row['heure']}<br>
<b>🚗 Accident</b> : {row['type_acci']}<br>
"""
        if not row['type_colli'].isdigit():
            popup_content += f"<b>🚨 Collision</b> : {row['type_colli']}<br>"

        if "Nuit" in row['luminosite']:
            emoji_lum = "🌑"
        else:
            emoji_lum = "☀️"

        popup_content += f"<b>{emoji_lum} Luminosité</b> : {row['luminosite']}"
        color = couleurs_par_commune.get(row['commune'], 'blue')
        folium.Marker(location=[row['geometry'].y, row['geometry'].x], popup=popup_content, parse_html=True, icon=folium.Icon(color=color)).add_to(m)

    # Ajout des radars que du 92
    radars_92 = radars[radars['departement'] == '92']
    for index, row in radars_92.iterrows():
        popup_content = f"""
<div style='white-space: pre-wrap; width: 200px;'>
"""

        icon_name = 'assets/radar_fixe.png'

        if (row['type'] != ''):
            popup_content += f"<b>🚨 {row['type']}</b><br>"
            if (row['type'] == 'Radar feu rouge'):
                icon_name = 'assets/radar_feu_rouge.png'
                

        if not pd.isna(row['route']) and isinstance(row['route'], str):
            popup_content += f"<b>🛣️ Route</b> : {row['route']}<br>"

        if not pd.isna(row['vitesse_vehicules_legers_kmh']) and isinstance(row['vitesse_vehicules_legers_kmh'], str):
            popup_content += f"<b>💨 Vitesse max</b> : {row['vitesse_vehicules_legers_kmh']} km/h<br>"

        icon = folium.CustomIcon(icon_image=icon_name, icon_size=(64, 64))
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_content, max_width='100%'),
            parse_html=True,
            icon=icon
        ).add_to(m)

    html_string = m.get_root().render().split('\n', 1)[1]

    # Modify the HTML string to set the height
    html_string = html_string.replace('<iframe', f'<iframe height="500px"')
        
    return html_string

# Callback pour créer la carte choroplèthe
def create_choropleth_map() -> str:
    center_lat = accident['geometry'].apply(lambda geom: geom.y).mean()
    center_lon = accident['geometry'].apply(lambda geom: geom.x).mean()

    m = folium.Map(location=[center_lat,center_lon], zoom_start=13)

    accident_count = accident.groupby('code_insee').size().reset_index(name='nbAccidents')

    folium.Choropleth(
        geo_data=geo_data_92,                              # geographical data
        name='choropleth',
        data=accident_count,                                  # numerical data
        columns=['code_insee', 'nbAccidents'],                     # numerical data key/value pair
        key_on='feature.properties.code',       # geographical property used to establish correspondance with numerical data
        fill_color='YlOrRd',  
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Nombre d\'accidents'
    ).add_to(m)

    # ajout des auto-écoles
    for index, row in driving_schools.iterrows():
        popup_content = f"""
<div style='white-space: pre-wrap; width: 200px;'>
<b>🏫 Nom</b> : {row['name']}<br>
<b>⭐ Note</b> : {row['grade']}/5
"""
        
        folium.Marker(location=[row['geometry'].y, row['geometry'].x], popup=folium.Popup(popup_content, max_width='100%'), parse_html=True, icon=folium.Icon(color='green')).add_to(m)

    legend_html = """
<div style="position: fixed; 
            top: 10px; 
            left: 50px;  
            border:2px solid grey; 
            z-index:9999; 
            font-size:14px;
            background-color: white;">
    <div style="color: green;">🏫 Auto école </div>
</div>
"""

    m.get_root().html.add_child(folium.Element(legend_html))

    html_string = m.get_root().render().split('\n', 1)[1]

    # Modify the HTML string to set the height
    html_string = html_string.replace('<iframe', f'<iframe height="500px" style="border: 0;"')

    return html_string

if __name__ == "__main__":
    asyncio.run(main())
    app.run_server(debug=True)
