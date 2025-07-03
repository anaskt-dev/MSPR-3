# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import database
import models
from routes import router as api_router
import auth
import data_loader
from sqlalchemy import text

app = FastAPI(title="MSPR API IA Pandémies")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    # Initialise la base de données (création tables)
    database.init_db()

    # Import automatique des données si la table est vide
    db = database.SessionLocal()
    try:
        result = db.execute(text("SELECT COUNT(*) FROM data")).scalar()
        if result == 0:
            print("Importation des données initiales...")
            data_loader.import_data_from_csv(db)
            print("Import terminé.")
        else:
            print("Données déjà présentes, import ignoré.")
    except Exception as e:
        print(f"Erreur lors de l'import initial des données : {str(e)}")
    finally:
        db.close()

# Inclut les routeurs sous /api
app.include_router(api_router, prefix="/api")
app.include_router(auth.router, prefix="/api")
