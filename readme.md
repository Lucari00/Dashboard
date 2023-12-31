# User Guide

## Déploiement et Utilisation du Dashboard

Pour déployer et utiliser le dashboard, suivez les étapes ci-dessous :

### Prérequis

Assurez-vous d'avoir les éléments suivants installés sur votre machine :

- Python (version 3.6 ou supérieure)
- Pip (gestionnaire de paquets Python)

### Étapes d'installation

1. Téléchargez le code source du dashboard depuis le [repository GitHub](https://github.com/Lucari00/Dashboard.git).

2. Naviguez vers le répertoire du projet via le terminal ou l'invite de commande.

3. Installez les dépendances en exécutant la commande suivante :
   ```bash
   pip install -r requirements.txt
   ```

### Exécution du Dashboard

1. Assurez-vous d'être toujours dans le répertoire du projet.

2. Exécutez le fichier `main.py` à l'aide de la commande suivante :
   ```bash
   python main.py
   ```

3. Le dashboard sera accessible via un navigateur web à l'adresse [http://127.0.0.1:8050/](http://127.0.0.1:8050/).

# Rapport d'Analyse

- Dans la première carte, nous pouvons observer la localisation des accidents par mois ainsi que la position des radars. D'après cette carte, nous ne pouvons pas déduire de corrélation directe entre les accidents et les radars. En effet, les radars n'opèrent que sur une route dans un sens de circulation et il est difficile de distinguer ces informations sur la carte.
Cependant, nous pouvons remarquer une concentration des accidents sur les grands axes, échangeurs et grosses intersections.

- Ensuite, l'histogramme nous permet de voir l'évolution du nombre d'accidents par mois tout au long de l'année. Nous pouvons noter une baisse d'accidents au mois d'août sur toutes les années enregistrées. Nous pouvons conjecturer que les Altoséquanais partent plus en vacances au mois d'août. Néanmoins, les départs et retours de vacances sont aussi caractéristiques de plus de circulation et donc d'accidents. Une autre possibilité est que la météo plus clémente de ce mois rend les conditions de circulation plus sûre.
En mars, avril, mai, novembre 2020 et en février 2021, les baisses du nombre d'accidents sont dues aux confinements, avec la plus forte baisse au milieu du premier. Mais il n'y a pas de baisse en dehors des confinements, alors qu'on pourrait s'y attendre avec le développement du télétravail.

- Le graphique suivant nous montre que la répartition des accidents dans la journée est très similaire pour toutes les années. La majorité des accidents se passe la journée, avec un pic aux heures de pointe (8h-9h et 17h-19h).

- Comme la répartition est la même dans la journée en fonction des années, nous avons fait l'histogramme suivant pour tout l'échantillon d'accidents. Grâce à celui-ci, nous vérifions les statistiques de la sécurité routière qui sont que 1/4 des accidents mortels se passent entre 2h et 6h. Il y a effectivement une significative augmentation de la gravité des accidents et de la mortalité pendant la nuit.

- Enfin, sur la dernière carte, les villes où se passent le plus d'accidents (plus de 2600 sur la période) sont Nanterre, Boulogne-Billancourt et Gennevilliers. Nanterre et Boulogne sont les deux villes les plus peuplées du 92, ce qui explique ce nombre. Gennevilliers, bien que moins peuplée, a des routes dangereuses puis l'A86 et le Viaduc sont des axes majeurs du Nord-Ouest parisien. Pour finir, le nombre d'auto écoles dans une ville ne semble pas être corrélé avec le nombre d'accidents dans celle-ci.
Pendant tout le temps de développement du dashboard, une auto école était présente en Egypte. En vérifiant sur le site où nous récupérons les données : [vroomvroom.fr](https://www.vroomvroom.fr/auto-ecoles/hauts-de-seine/asnieres-sur-seine), nous pouvions voir qu'il donnait bien une auto école en Egypte. Nous avions décidé de la laisser pour voir si dans le futur, le site aurait changé sa localisation, ce qui est effictement le cas.

# Developer Guide

## Architecture du Code

Le code du dashboard est structuré de la façon suivante:

```mermaid
flowchart TD
    subgraph get_data.py
        a1(get_data.py)
        a2(get_scraping_data)
        a3(get_data_from_internet)
        a4(lighten_data)
        a5(all data retrieved)
    end

    subgraph scraping.py
        b2(create_firefox_browser)
        b3(get_cities)
        b4(wait_for_element_loading)
        b5(get_driving_schools)
        b6(charge internet page)
    end

    subgraph main.py
        c1(main.py)
        c2(check if data is present)
        c3(create_dashboard)
        c4(callback)
        c5(Site uptaded)
    end

    a1 --> a3
    a1 --> a2
    a3 -->|If needed| a4
    a3 --> a5
    a4 --> a5
    a2 --> b2
    b2 --> b3
    b3 --> b6
    b6 --> b4
    b4 --> b5
    b5 --> b6
    b6 -->|If no more page to analyse| a5
    c2{Is Data present?} -->|Yes| c3
    c2 -->|No| a1
    a5{Is all data retrieved?} -->|Yes| c3
    c1 --> c2
    c3 --> c4
    c4{Wait for callback} -->|Callback| c5
    c5 --> c4
```

### Description de chaque fichier important

- `main.py` : Fichier principal contenant la configuration du dashboard, les callbacks et les fonctions de création des cartes, des histogrammes et du graphique.
- `get_data.py` : Fichier contenant les fonctions permettant de télécharger et de traiter les données sur les accidents.
- `scraping.py` : Fichier contenant l'extraction de données sur un site internet, ici [vroomvroom.fr](https://www.vroomvroom.fr/auto-ecoles/hauts-de-seine/).
- `requirements.txt`: Fichier contenant toutes les bibliothèques dont le dashboard a besoin pour être exécuté.
- `assets/styles.css`: Fichier contenant le style du site, particulièrement le body du html pour faciliter la configuration globale du site.

## Modification ou Extension du Code

- **Personnalisation des couleurs :** Vous pouvez ajuster les couleurs utilisées possibles pour représenter chaque commune en modifiant la variable `couleurs_acceptees` dans le fichier `main.py`. Vous avez la possibilité d'ajuster les couleurs utilisées pour représenter chaque commune en modifiant la variable couleurs_acceptees dans le fichier main.py. Ces couleurs seront attribuées de manière aléatoire à chaque commune au début de chaque exécution du programme.

- **Ajout de nouvelles fonctionnalités :** Pour ajouter de nouvelles fonctionnalités au dashboard, vous pouvez ajouter dans le `main.py` à la variable `app.layout` tous les éléments html que vous souhaitez. Ensuite, vous pouvez aussi rajouter vos propres graphiques ou cartes. Pour simplifier la structure du code, nous vous recommandons de créer une fonction qui va renvoyer l'élément à afficher. Pour ajouter des éléments dynamiques, créer un `@app.callback`, avec les entrées et sorties qu'il vous faut.

- **Extension des fonctionnalités de récupération de données :** Si vous avez besoin de récupérer des données supplémentaires ou de les traiter différemment, vous pouvez modifier les fonctions du fichier `get_data.py`. Il suffit de rajouter les tests dans le
`with ThreadPoolExecutor(max_workers=3) as executor:` avec des lignes comme suit : 
```python
if not path.exists("data/votre-nom-de-fichier.extension"):
   executor.submit(fonction, parametre1, parametre2,)
else:
   print("Le fichier votre-nom-de-fichier existe déjà !")
```
* `fonction` peut être `def get_data_from_internet(url: str, path: str, filename: str, lourd: bool) -> None:` qui va télécharger depuis l'`url` donnée et le sauvegarder au `path` et au `filename`(avec extension) donné. Le paramètre `lourd` sera forcément à `false`.
* `fonction` peut aussi être une fonction que vous pouvez créer et faire du scraping depuis le fichier `scraping.py` où il y a toutes les fonctions dont vous avez besoin pour scraper le site que vous voulez.

Vous pouvez maintenant étendre le dashboard comme bon vous semble !

# Copyright
Nous déclarons sur l’honneur que le code fourni a été produit par nous même, à l’exception de la ligne ci dessous :
```python
  ssl._create_default_https_context = ssl._create_unverified_context
```

Source : https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
