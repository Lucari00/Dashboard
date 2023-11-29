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

Le dashboard visualise les accidents de la route dans les Hauts-de-Seine en avril 2019. Voici quelques conclusions tirées des données :

- La majorité des accidents semble être concentrée dans certaines communes, identifiables par les couleurs sur la carte.
- L'histogramme présente la distribution du nombre d'accidents par mois pour l'année sélectionnée, offrant une vue d'ensemble des tendances.

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