# backend/main.py

# Importe la classe FastAPI pour créer l'application web.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Importe le module `database` qui contient la logique d'initialisation de la base de données.
import database
# Importe le module 'models' pour s'assurer que les modèles de base de données sont reconnus par SQLAlchemy avant l'initialisation de la base de données.
import models
# Importe les routeurs définis dans `routes.py` pour les endpoints de l'API (données, prédiction).
from routes import router as api_router
# Importe le routeur d'authentification défini dans `auth.py`.
from auth import router as auth_router
import data_loader
from sqlalchemy import text

# Crée une instance de l'application FastAPI avec un titre descriptif.
app = FastAPI(title="MSPR API IA Pandémies")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Définit un événement de démarrage qui sera exécuté au lancement de l'application.
@app.on_event("startup")
def on_startup():
    # Initialise la base de données lorsque l'application démarre.
    # Cela inclut généralement la création des tables si elles n'existent pas.
    database.init_db()

# Import automatique des données si la base est vide
def import_initial_data():
    db = database.SessionLocal()
    try:
        # Vérifie si des données existent déjà en utilisant text() pour la requête SQL brute
        result = db.execute(text("SELECT COUNT(*) FROM data")).scalar()
        if result == 0:
            data_loader.import_data_from_csv(db)
    except Exception as e:
        print(f"Erreur lors de l'import initial des données : {str(e)}")
    finally:
        db.close()

# Importe les données au démarrage
import_initial_data()

# Inclut le routeur des API générales sous le préfixe '/api'.
# Toutes les routes définies dans `routes.py` seront accessibles via /api/your-endpoint.
app.include_router(api_router, prefix="/api")
# Inclut le routeur d'authentification sous le même préfixe '/api'.
# Les routes d'authentification (ex: /api/login, /api/register) seront accessibles.
app.include_router(auth_router, prefix="/api") 