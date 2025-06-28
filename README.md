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

## 📊 Visualisations
- Graphiques interactifs (Plotly, PyDeck)
- Carte mondiale des cas Covid-19

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

## 🧪 Tests & Qualité
- Tests automatisés backend :
```bash
cd backend
python -m pytest tests/ -v
```
- Linting/formatage :
```bash
black .
flake8 .
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

---

**PandemIA – Anticiper aujourd'hui, protéger demain**

