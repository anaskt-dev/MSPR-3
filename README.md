# PandemIA – Plateforme Data & IA Covid-19

## 🚀 Présentation
PandemIA est une plateforme professionnelle de suivi, d'analyse et de prédiction de la pandémie de Covid-19. Elle combine un backend sécurisé (FastAPI) et un frontend moderne (Streamlit), avec authentification, visualisations avancées, prédiction IA et conformité RGPD.

---

## 🗂️ Structure détaillée du projet

```
MSPR AKRAM/
├── backend/
│   ├── __init__.py
│   ├── main.py              # Point d'entrée FastAPI
│   ├── auth.py              # Authentification JWT
│   ├── models.py            # Modèles SQLAlchemy
│   ├── schemas.py           # Schémas Pydantic
│   ├── routes.py            # Endpoints API
│   ├── database.py          # Configuration DB
│   ├── base.py              # Base SQLAlchemy
│   ├── data/
│   │   └── covid_cleaned.csv
│   ├── Dockerfile           # Docker backend
│   └── requirements.txt     # Dépendances backend
├── frontend/
│   ├── app.py               # Interface Streamlit
│   ├── auth.py              # Auth frontend
│   ├── logo-pandemia.png
│   ├── Dockerfile           # Docker frontend
│   └── requirements.txt     # Dépendances frontend
├── docker-compose.yml       # Orchestration des services
└── README.md                # Documentation
```

Chaque dossier/fichier a un rôle précis :
- **backend/** : API FastAPI, gestion des utilisateurs, modèles, base de données, endpoints sécurisés.
- **frontend/** : Application Streamlit, interface utilisateur, authentification, visualisations.
- **docker-compose.yml** : Orchestration des conteneurs backend/frontend.
- **README.md** : Documentation complète du projet.

---

## 🏗️ Architecture technique
- **Backend** : FastAPI, SQLite, SQLAlchemy, Pydantic, JWT, endpoints RESTful
- **Frontend** : Streamlit, Plotly, PyDeck, multilingue, gestion RGPD
- **Docker** : Conteneurs séparés, communication optimisée, déploiement facile

---

## 🐳 Installation & Lancement
### Prérequis
- Docker & Docker Compose
- Git
- Python 3.9+ (pour dev local)

### Lancement rapide
```bash
# Cloner le projet
git clone <url-du-repo>
cd MSPR-AKRAM
# Lancer avec Docker
docker-compose up --build
```

### Développement local
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
# Frontend
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

---

## 🔐 Sécurité & RGPD
- Authentification JWT obligatoire pour accéder aux données/prédictions
- Validation stricte des entrées (Pydantic)
- Accès et langues adaptés selon le pays (France, Suisse, US)
- Respect des règles RGPD (fonctionnalités et langues dynamiques)

---

## 📊 Visualisations & Graphes IA
- Page dédiée "Graphes IA" : toutes les visualisations générées par l'IA et l'analyse des données Covid-19 (accès via le menu)
- Affichage professionnel en grille (2 graphes par ligne)
- Présentation vidéo intégrée (dossier `frontend/image_models/telecharger.mp4`)
- Graphiques interactifs (Plotly)

## ♿ Accessibilité & UX
- Thème sombre uniforme
- Navigation clavier et contrastes respectés
- Footer EPSI/RGPD sur toutes les pages
- Checklist accessibilité (Lighthouse, axe DevTools)

---

## 🤖 Prédiction IA
- Prédiction du nombre de cas futurs par pays et date
- Sélection intuitive du pays et de la date
- Affichage du score de confiance
- Historique des prédictions possible

---

## 🌐 API Principale
| Endpoint                | Méthode | Description                        |
|------------------------|---------|------------------------------------|
| /api/register          | POST    | Inscription utilisateur            |
| /api/token             | POST    | Connexion (JWT)                    |
| /api/data              | GET     | Toutes les données Covid-19        |
| /api/data?country=XX   | GET     | Données filtrées par pays          |
| /api/predict           | POST    | Prédiction IA                      |

**Exemple de données :**
```json
{
  "date": "2024-01-01",
  "country": "France",
  "confirmed": 1000,
  "deaths": 10,
  "recovered": 900,
  "new_cases": 50
}
```

---

## 🤖 Intégration et fonctionnement du modèle IA

### Intégration des modèles
- Modèle de prédiction Prophet (sérialisé en `.pkl`).
- Les modèles sont stockés dans `backend/models_and_results/`.
- Lors d'une requête de prédiction, le backend charge dynamiquement le modèle Prophet.

### Fonctionnement de la prédiction
- L'API `/api/predict` reçoit un payload avec :
  - le pays
  - le nombre de jours à prédire
  - la date de référence historique (pour Prophet)
- Le backend prépare les données, applique les transformations nécessaires (ex : création de la colonne `cases_log` pour Prophet), et effectue la prédiction.
- Le résultat est renvoyé sous forme de liste de valeurs prédites, avec la date correspondante.

**Exemple de payload pour `/api/predict`**
```json
{
  "country": "France",
  "days": 7,
  "prediction_type": "cases",
  "reference_date": "2020-07-01"
}
```

---

## 🧪 Stratégie de tests

Le projet est testé à plusieurs niveaux pour garantir robustesse, sécurité et accessibilité :

- **Tests unitaires** : chaque fonction critique (auth, prédiction, transformation) est testée indépendamment avec pytest et des mocks.
- **Tests d'intégration** : les endpoints FastAPI sont testés avec une base SQLite temporaire, en simulant les appels réels.
- **Tests d'accessibilité** : audit via Lighthouse, axe DevTools, navigation clavier.

### Commandes utiles

```bash
# Lancer tous les tests backend
PYTHONPATH=. pytest backend/tests/ --maxfail=3 --disable-warnings -v

# Générer un rapport de couverture
pytest --cov=backend backend/tests/
pytest --cov=backend --cov-report=html backend/tests/
# Ouvre htmlcov/index.html dans ton navigateur

# Audit accessibilité (frontend)
# Ouvre l'app dans Chrome > Lighthouse > Accessibility > Générer le rapport
```

---

## 👥 Auteurs
- Anas – Développeur IA
- Laura – Fullstack & DevOps
- Akram – DevOps
- Romance – Fullstack

---

## 📎 Liens utiles
- [Streamlit](https://streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Prophet](https://facebook.github.io/prophet/)
- [Pillow](https://python-pillow.org/)

---

**PandemIA – Anticiper aujourd'hui, protéger demain**

