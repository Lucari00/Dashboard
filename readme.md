# User Guide

## Déploiement et Utilisation du Dashboard

Pour déployer et utiliser le dashboard sur une autre machine, suivez les étapes ci-dessous :

### Prérequis

Assurez-vous d'avoir les éléments suivants installés sur votre machine :

- Python (version 3.6 ou supérieure)
- Pip (gestionnaire de paquets Python)

### Étapes d'installation

1. Téléchargez le code source du dashboard depuis le [repository GitHub](https://github.com/Lucari00/Dashboard.git).

2. Naviguez vers le répertoire du projet via le terminal ou l'invite de commande.

3. Installez les dépendances en exécutant la commande suivante :
   ```
   pip install -r requirements.txt
   ```

### Exécution du Dashboard

1. Assurez-vous d'être toujours dans le répertoire du projet.

2. Exécutez le fichier `main.py` à l'aide de la commande suivante :
   ```
   python main.py
   ```

3. Le dashboard sera accessible via un navigateur web à l'adresse [http://127.0.0.1:8050/](http://127.0.0.1:8050/).

4. Utilisez les menus déroulants pour sélectionner l'année et le mois afin de visualiser les données sur les accidents de la route dans les Hauts-de-Seine.

# Rapport d'Analyse

- Dans la première carte, nous pouvons observer la localisation des accidents par mois ainsi que la position des radars. D'après cette carte, nous ne pouvons pas déduire de corrélation directe entre les accidents et les radars. En effet, les radars n'opèrent que sur une route dans un sens de circulation et il est difficile de distinguer ces informations sur la carte.
Cependant, nous pouvons remarquer une concentration des accidents sur les grands axes, échangeurs et grosses intersections.

- Ensuite, l'histogramme nous permet de voir l'évolution du nombre d'accidents par mois tout au long de l'année. Nous pouvons noter une baisse d'accidents au mois d'août sur toutes les années enregistrées. Nous pouvons conjecturer que les Altoséquanais partent plus en vacances au mois d'août. Néanmoins, les départs et retours de vacances sont aussi caractéristiques de plus de circulation et donc d'accidents. Une autre possibilité est que la météo plus clémente de ce mois rend les conditions de circulation plus sûre.
En mars, avril, mai, novembre 2020 et en février 2021, les baisses du nombre d'accidents sont dues aux confinements, avec la plus forte baisse au milieu du premier. Mais il n'y a pas de baisse en dehors des confinements, alors qu'on pourrait s'y attendre avec le développement du télétravail.

- Le graphique suivant nous montre que la répartition des accidents dans la journée est très similaire pour toutes les années. La majorité des accidents se passe la journée, avec un pic aux heures de pointe (8h-9h et 17h-19h).

- Comme la répartition est la même dans la journée en fonction des années, nous avons fait l'histogramme suivant pour tout l'échantillon d'accidents. Grâce à celui-ci, nous vérifions les statistiques de la sécurité routière qui sont que 1/4 des accidents mortels se passent entre 2h et 6h. Il y a effectivement une significative augmentation de la gravité des accidents et de la mortalité pendant la nuit.

- Enfin, sur la dernière carte, les villes où se passent le plus d'accidents (plus de 2600 sur la période) sont Nanterre, Boulogne-Billancourt et Gennevilliers. Nanterre et Boulogne sont les deux villes les plus peuplées du 92, ce qui explique ce nombre. Gennevilliers, bien que moins peuplée, a des routes dangereuses puis l'A86 et le Viaduc sont des axes majeurs du Nord-Ouest parisien. Pour finir, le nombre d'auto écoles dans une ville ne semble pas être corrélé avec le nombre d'accidents dans celle-ci
Nous sommes au courant d'une auto école étant présente en Egypte. En vérifiant sur le site où nous récupérons les données : [vroomvroom.fr](https://www.vroomvroom.fr/auto-ecoles/hauts-de-seine/asnieres-sur-seine), nous pouvons voir qu'il donne bien une auto école en Egypte. Nous avons décidé la laisser pour voir si dans le futur, le site change sa localisation.

# Developer Guide

## Architecture du Code

Le code du dashboard est structuré comme suit :

- `main.py` : Fichier principal contenant la configuration du tableau de bord Dash, les callbacks et les fonctions de création de la carte et de l'histogramme.
- `get_data.py` : Fichier contenant les fonctions permettant de télécharger et de traiter les données sur les accidents.

## Modification ou Extension du Code

- **Personnalisation des couleurs :** Vous pouvez ajuster les couleurs utilisées pour représenter chaque commune en modifiant la variable `couleurs_acceptees` dans le fichier `main.py`.

- **Ajout de nouvelles fonctionnalités :** Pour ajouter de nouvelles fonctionnalités au tableau de bord, vous pouvez créer de nouveaux éléments graphiques dans le fichier `main.py` en utilisant la bibliothèque Dash et Plotly.

- **Extension des fonctionnalités de récupération de données :** Si vous avez besoin de récupérer des données supplémentaires ou de les traiter différemment, vous pouvez modifier les fonctions du fichier `get_data.py`.

N'hésitez pas à explorer et à expérimenter pour personnaliser le dashboard en fonction de vos besoins spécifiques.