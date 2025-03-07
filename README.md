# TempBlanket
TempBlanket est un outil de gestion d'avancement d'une couverture au crochet, se basant sur des données de températures sur l'année 2024.
Elle permet de lister les éléments de couverture à réaliser et d'indiquer ceux déjà fait.

## Installation
Dépendance : python 3.12.0, pip 24.1.1
1. Cloner le repertoire
2. Créer un environnement virtuel puis l'activer
    ```
    python -m venv env
    ```
3. Installer les librairies
    ```
    pip install -r requirements.txt
    ```

## Front-End
Toute l'interface de l'outil a été developpée en utilisant la librairie PySide6 et Qt Designer.

Pour charger un fichier .ui, vous pouvez utiliser la méthode load_ui dans view/utilitaires.

Les ressources du logiciel sont stockées dans le dossier assets. Les icons ont été récupérés avec google icons.
Le fichier .qrc liste toutes ces ressources, il est compilé en lançant la commande :  
    ```
    pyside6-rcc resources.qrc -o view\resources_rc.py
    ```

Ajoutez ```import view.resources_rc``` dans tout fichier ayant besoin d'au moins une de ces ressources.

