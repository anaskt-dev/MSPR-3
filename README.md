# 🌍 MSPR - Système de Prédiction et Analyse des Données COVID-19 avec IA et RGPD

## 📝 Description

**PandemIA** est une application web interactive conçue pour le suivi en temps réel et la prédiction de l'évolution de la pandémie de COVID-19. Elle offre une plateforme complète aux acteurs de la santé et au grand public pour visualiser les données historiques, anticiper les tendances futures grâce à l'intelligence artificielle, et prendre des décisions éclairées. Le projet met un accent particulier sur la conformité au **RGPD**, en adaptant les fonctionnalités et la langue en fonction du pays sélectionné par l'utilisateur.

## ✨ Fonctionnalités Principales

### 📊 Analyse de Données
- Visualisation interactive des données COVID-19 mises à jour quotidiennement.
- Graphiques dynamiques (cas confirmés, décès, guérisons, nouveaux cas, taux de mortalité/guérison).
- Métriques clés et aperçu des tendances cumulatives.
- Filtrage des données par pays avec respect des règles RGPD.

### 🤖 Prédictions IA
- **Prédiction simulée** du nombre de cas futurs pour un pays et une date donnée.
- Conception modulaire prête à l'intégration d'un modèle d'apprentissage automatique plus avancé.
- Interface intuitive pour la sélection des paramètres de prédiction.
- Score de confiance (exemple).

### 🔐 Système d'Authentification
- Inscription et connexion sécurisées des utilisateurs.
- Gestion des sessions utilisateur avec jetons JWT.
- Protection des routes API sensibles nécessitant une authentification.
- Gestion des droits d'accès pour certaines fonctionnalités (ex: prédiction).

### 🌐 Conformité RGPD & Internationalisation
- **Choix du pays** influençant les options de menu disponibles.
- **Sélection dynamique de la langue** de l'interface utilisateur (Français, Anglais, Italien, Allemand) basée sur le pays sélectionné.

## 🛠️ Technologies Utilisées

### Backend (API RESTful)
- **FastAPI** : Framework web Python moderne, rapide et performant pour la création d'APIs.
- **SQLAlchemy** : Toolkit SQL et Object-Relational Mapper (ORM) pour interagir avec la base de données.
- **Pydantic** : Bibliothèque de validation des données et de sérialisation, utilisée par FastAPI pour la robustesse des schémas.
- **python-jose & passlib (bcrypt)** : Pour l'implémentation sécurisée de l'authentification basée sur les jetons Web JSON (JWT) et le hachage des mots de passe.
- **SQLite** : Base de données légère et embarquée, idéale pour le développement et la démonstration.
- **Pandas** : Pour la manipulation et l'importation efficiente des données CSV.
- **Scikit-learn** : (Optionnel/À justifier si non utilisé pour un vrai modèle) Bibliothèque d'apprentissage automatique pour une future intégration de modèles de prédiction.

### Frontend (Interface Utilisateur)
- **Streamlit** : Framework Python open-source pour la création rapide d'applications web interactives de science des données.
- **Plotly.graph_objects** : Bibliothèque graphique interactive pour des visualisations de données complexes et personnalisées.
- **PyDeck** : Framework de visualisation géospatiale pour la création de cartes 3D interactives.
- **Pandas** : Essentiel pour la manipulation et la préparation des données côté client.
- **Streamlit-option-menu** : Composant Streamlit pour une barre de navigation latérale moderne.
- **Requests** : Bibliothèque HTTP pour la communication avec l'API backend.

## 🚀 Installation

Pour lancer le projet localement, suivez ces étapes :

1.  **Cloner le Repository**
    ```bash
    git clone [URL_DU_REPO]
    cd MSPR-AKRAM # Assurez-vous d'être dans le dossier racine du projet
    ```

2.  **Créer un Environnement Virtuel**
    Il est recommandé d'utiliser un environnement virtuel pour gérer les dépendances du projet :
    ```bash
    python -m venv venv
    source venv/bin/activate  # Pour Linux / macOS
    # ou
    .\venv\Scripts\activate  # Pour Windows (dans PowerShell ou Cmd)
    ```

3.  **Installer les Dépendances**
    Assurez-vous que votre environnement virtuel est activé, puis installez toutes les bibliothèques requises :
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialiser la Base de Données et Importer les Données**
    Ce script créera la base de données SQLite (`mspr.db`) et importera les données du fichier `covid_cleaned.csv`.
    ```bash
    python backend/import_csv.py
    ```

## 💻 Utilisation

Après l'installation, vous devez démarrer le backend et le frontend séparément.

1.  **Démarrer le Backend (API)**
    Ouvrez un nouveau terminal et naviguez vers le dossier `backend` :
    ```bash
    cd backend
    uvicorn main:app --reload --port 8000 # Utilisez le port 8000 par défaut ou celui que vous préférez
    ```
    L'API sera accessible à `http://localhost:8000`. Sa documentation interactive (Swagger UI) sera disponible à `http://localhost:8000/docs`.

2.  **Démarrer le Frontend (Application Streamlit)**
    Ouvrez un autre terminal et naviguez vers le dossier `frontend` :
    ```bash
    cd frontend
    streamlit run app.py
    ```
    L'application Streamlit sera accessible à `http://localhost:8501`.

## 📁 Structure du Projet

```
MSPR-AKRAM/
├── backend/
│   ├── __init__.py
│   ├── main.py               # Point d'entrée de l'API FastAPI
│   ├── models.py             # Définition des modèles de base de données (SQLAlchemy)
│   ├── schemas.py            # Schémas de données pour la validation (Pydantic)
│   ├── routes.py             # Définition des points d'API (routes)
│   ├── auth.py               # Logique d'authentification et JWT
│   ├── database.py           # Configuration de la connexion à la base de données
│   ├── import_csv.py         # Script d'importation des données depuis le CSV
│   ├── mspr.db               # Fichier de base de données SQLite (généré)
│   └── data/                 # Dossier contenant le fichier de données CSV
│       └── covid_cleaned.csv
├── frontend/
│   ├── app.py                # Application Streamlit principale
│   ├── auth.py               # Fonctions d'authentification et appels API pour le frontend
│   └── logo-pandemia.png     # Logo de l'application
├── requirements.txt          # Liste des dépendances Python
└── README.md                 # Ce fichier de documentation
```

## 🔒 Sécurité et Conformité

-   **Authentification JWT** : Jeton Web JSON pour l'accès sécurisé aux ressources.
-   **Hachage des mots de passe** : Utilisation de Bcrypt via `passlib` pour stocker les mots de passe de manière sécurisée (non en clair).
-   **Validation des données** : Les schémas Pydantic assurent que toutes les données entrantes et sortantes respectent les formats attendus.
-   **Protection contre les injections SQL** : L'utilisation d'un ORM comme SQLAlchemy aide à prévenir les vulnérabilités aux injections SQL.
-   **Respect des règles RGPD** :
    -   Gestion des préférences linguistiques et des fonctionnalités spécifiques à chaque pays.
    -   Stockage minimal des données utilisateur et utilisation de données de pandémie anonymisées/agrégées.
    -   (Note pour la présentation: La `SECRET_KEY` est pour la démo, en production elle serait sécurisée via des variables d'environnement).

## 📈 Fonctionnalités d'Analyse et de Visualisation

-   **Visualisation des tendances** : Graphiques interactifs pour suivre l'évolution des cas confirmés, décès, guérisons et nouveaux cas.
-   **Calcul des métriques clés** : Taux de mortalité et de guérison calculés dynamiquement.
-   **Analyse comparative entre pays** : Possibilité de visualiser les données pour différents pays (selon les règles RGPD).
-   **Carte interactive** : Visualisation globale des taux de cas par pays grâce à PyDeck (Note pour la présentation: utilisation de coordonnées simplifiées pour la démo, une approche GeoJSON serait plus robuste).

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1.  Fork le projet
2.  Créer une branche pour votre fonctionnalité
3.  Commiter vos changements
4.  Pousser vers la branche
5.  Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Auteurs

-   [Votre Nom(s) / Noms de l'équipe]

## 🙏 Remerciements

-   [Toute personne ayant aidé ou contribué]
-   [Bibliothèques / Frameworks spécifiques non mentionnés ci-dessus si nécessaire]
-   [Sources de données exactes si vous avez des liens (ex: WHO, Johns Hopkins University, etc.)]

## 🐳 Déploiement avec Docker (Optionnel - Avancé)

### Prérequis
-   Docker
-   Docker Compose

### Déploiement Rapide
1.  **Cloner le Repository**
    ```bash
    git clone [URL_DU_REPO]
    cd MSPR-AKRAM
    ```

2.  **Construire et Démarrer les Conteneurs**
    ```bash
    docker-compose up --build
    ```

3.  **Accéder à l'Application**
    -   Frontend : `http://localhost:8502` (Note: le port peut varier selon votre configuration Docker Compose, vérifiez votre `docker-compose.yml`)
    -   API Documentation : `http://localhost:8001/docs` (Note: le port peut varier)

### Structure Docker
-   **Backend** : Service FastAPI exposé sur un port (par ex. 8001).
-   **Frontend** : Service Streamlit exposé sur un port (par ex. 8501 ou 8502 si le port par défaut est pris).
-   **Base de données** : SQLite persistante via volume Docker.
-   **Réseau** : Communication inter-services via réseau Docker.

### Commandes Docker Utiles
```bash
# Démarrer les services
docker-compose up

# Démarrer en mode détaché
docker-compose up -d

# Arrêter les services
docker-compose down

# Voir les logs
docker-compose logs -f

# Reconstruire les images
docker-compose build
``` 