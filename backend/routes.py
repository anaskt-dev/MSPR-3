from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.orm import Session
import schemas
import models
import database
import auth
from typing import List, Optional
import logging
import ml_model
import numpy as np
import datetime
from datetime import date
import data_loader
from ml_model import predict_dispatch
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

# Authentification
@router.post("/register", response_model=schemas.UserOut)
def register(
    user: schemas.UserCreate, # Reçoit les données de l'utilisateur à créer, validées par le schéma UserCreate.
    db: Session = Depends(database.get_db) # Injecte une session de base de données.
):
    """Enregistre un nouvel utilisateur dans la base de données.
    Vérifie si le nom d'utilisateur ou l'email existe déjà pour éviter les doublons.
    Hache le mot de passe avant de sauvegarder l'utilisateur."""
    # Vérifie si un utilisateur avec le même nom d'utilisateur ou email existe déjà.
    db_user = db.query(models.User).filter((models.User.username == user.username) | (models.User.email == user.email)).first()
    if db_user:
        # Lève une exception HTTP 400 si l'utilisateur existe déjà.
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    # Hache le mot de passe avant de le stocker dans la base de données.
    hashed_password = auth.get_password_hash(user.password)
    # Crée une nouvelle instance du modèle User avec les données fournies.
    new_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password, country=user.country, is_admin=False)
    
    # Ajoute le nouvel utilisateur à la session de la base de données, commite et rafraîchit l'objet.
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return schemas.UserOut.from_orm(new_user)

# Utilisateur courant
@router.get("/me", response_model=schemas.UserOut)
def read_users_me(
    current_user: models.User = Depends(auth.get_current_user)
):
    """Récupère les informations de l'utilisateur actuellement authentifié. Cette route nécessite un jeton JWT valide."""
    return schemas.UserOut.from_orm(current_user)

# Données historiques
@router.post("/data", response_model=schemas.DataOut)
def add_data(
    data: schemas.DataIn, # Données COVID-19 à ajouter, validées par le schéma DataIn.
    db: Session = Depends(database.get_db), # Injecte une session de base de données.
    current_user: models.User = Depends(auth.get_current_user) # Assure que seul un utilisateur authentifié peut ajouter des données.
):
    """Ajoute de nouvelles entrées de données COVID-19 à la base de données.
    Requiert une authentification préalable."""
    db_data = models.Data(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return schemas.DataOut.from_orm(db_data)

@router.get("/data", response_model=List[schemas.DataOut])
def read_data(
    country: Optional[str] = Query(None), # Paramètre de requête facultatif pour filtrer les données par pays.
    skip: int = 0, # Paramètre pour la pagination : nombre d'éléments à ignorer.
    limit: int = 10000, # Paramètre pour la pagination : nombre maximal d'éléments à retourner.
    db: Session = Depends(database.get_db) # Injecte une session de base de données.
):
    """Récupère les données historiques de la pandémie. Peut être filtré par pays et paginé.
    Accessible publiquement (pas de dépendance d'authentification)."""
    query = db.query(models.Data)
    if country:
        query = query.filter(models.Data.country == country) # Applique le filtre par pays si spécifié.
    # Exécute la requête avec les paramètres de pagination et retourne tous les résultats.
    data = query.offset(skip).limit(limit).all()
    return [schemas.DataOut.from_orm(d) for d in data]

# Récupérer tous les pays uniques
@router.get("/countries", response_model=List[str])
def get_all_countries(
    db: Session = Depends(database.get_db) # Injecte une session de base de données.
):
    """Récupère une liste de tous les pays uniques présents dans les données COVID-19.
    Les pays sont triés par ordre alphabétique. Accessible publiquement."""
    # Récupère les noms de pays distincts et les trie.
    countries = db.query(models.Data.country).distinct().order_by(models.Data.country).all()
    return [country[0] for country in countries] # Retourne une liste de chaînes de caractères (noms de pays).

# Endpoint pour charger/recharger les données depuis le CSV
@router.post("/load-data")
def load_data(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Charge les données du fichier CSV dans la base de données.
    Efface les données existantes avant l'import.
    """
    result = data_loader.import_data_from_csv(db)
    
    if result["status"] == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'importation des données : {result['message']}"
        )
        
    return result

# --- CRUD par ID (corrigé) ---
@router.get("/data/id/{id}", response_model=schemas.DataOut)
def get_data_by_id(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    data = db.query(models.Data).filter(models.Data.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return schemas.DataOut.from_orm(data)

@router.put("/data/id/{id}", response_model=schemas.DataOut)
def update_data(id: int, update: dict, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    data = db.query(models.Data).filter(models.Data.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    for key, value in update.items():
        if hasattr(data, key):
            setattr(data, key, value)
    db.commit()
    db.refresh(data)
    return schemas.DataOut.from_orm(data)

@router.delete("/data/id/{id}")
def delete_data(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    data = db.query(models.Data).filter(models.Data.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    db.delete(data)
    db.commit()
    return {"detail": "Data deleted"}

# --- GET par pays (corrigé) ---
@router.get("/data/country/{country}", response_model=List[schemas.DataOut])
def get_data_by_country(country: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    data = db.query(models.Data).filter(models.Data.country == country).all()
    if not data:
        raise HTTPException(status_code=404, detail="No data found for this country")
    return [schemas.DataOut.from_orm(d) for d in data]

# --- Correction du endpoint de prédiction ---
@router.post("/predict", response_model=schemas.PredictionOut)
def get_prediction(
    prediction_in: schemas.PredictionIn, # Données d'entrée pour la prédiction, validées par PredictionIn.
    db: Session = Depends(database.get_db), # Injecte une session de base de données.
    current_user: models.User = Depends(auth.get_current_user) # Assure que seul un utilisateur authentifié peut demander une prédiction.
):
    logger.info(f"[PREDICT] Payload reçu: {prediction_in.dict()}")
    """Effectue une prédiction basée sur le modèle IA choisi (Prophet ou LSTM)."""
    if prediction_in.days is None or prediction_in.days <= 0 or prediction_in.days > 30:
        raise HTTPException(status_code=422, detail="Le nombre de jours doit être entre 1 et 30.")
    if prediction_in.prediction_type not in ["cases", "deaths", "recovered"]:
        raise HTTPException(status_code=422, detail="Invalid prediction_type. Must be 'cases', 'deaths', or 'recovered'")
    
    # Gérer la date de référence historique
    reference_date = None
    if prediction_in.reference_date:
        try:
            reference_date = pd.to_datetime(prediction_in.reference_date).date()
        except:
            raise HTTPException(status_code=422, detail="Format de date de référence invalide. Utilisez le format YYYY-MM-DD.")
    else:
        # Date par défaut en 2020 si aucune date n'est fournie
        reference_date = date(2020, 7, 1)
    
    # Récupérer les données historiques du pays
    historical_data = db.query(models.Data).filter(models.Data.country == prediction_in.country).order_by(models.Data.date).all()
    if not historical_data:
        raise HTTPException(status_code=404, detail=f"No data found for {prediction_in.country} to make a prediction.")
    
    # Convertir en DataFrame
    df_data = []
    for d in historical_data:
        df_data.append({
            'date': d.date,
            'cases': d.confirmed,  # Renommer 'confirmed' en 'cases' pour Prophet/LSTM
            'deaths': d.deaths,
            'recovered': d.recovered,
            'new_cases': d.new_cases,
            'new_deaths': d.new_deaths,
            'new_recovered': d.new_recovered,
            'country': d.country
        })
    df = pd.DataFrame(df_data)

    # Calculer le taux de mortalité (%)
    if 'taux_mortalite' not in df.columns:
        df['taux_mortalite'] = (df['deaths'] / df['cases']) * 100
        df['taux_mortalite'] = df['taux_mortalite'].fillna(0)

    # Filtrer les données jusqu'à la date de référence
    df_filtered = df[df['date'] <= reference_date].copy()
    if len(df_filtered) == 0:
        raise HTTPException(status_code=422, detail=f"Aucune donnée disponible pour {prediction_in.country} jusqu'à la date {reference_date}.")
    
    # Log avancé pour debug pro
    logger.info(f"df_filtered shape: {df_filtered.shape}")
    logger.info(f"df_filtered columns: {df_filtered.columns}")
    if 'taux_mortalite' in df_filtered.columns:
        logger.info(f"df_filtered['taux_mortalite'] tail: {df_filtered['taux_mortalite'].tail()}")
    else:
        logger.warning("Colonne 'taux_mortalite' absente du DataFrame !")

    # Appeler le modèle Prophet (LSTM supprimé)
    try:
        forecast = predict_dispatch('prophet', df_filtered, prediction_in.days)
    except Exception as e:
        logger.error(f"Erreur lors de la prédiction Prophet : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction Prophet : {e}")
    
    # Retourner directement la valeur prédite comme taux de mortalité (%)
    predictions = []
    for i in range(prediction_in.days):
        pred_date = reference_date + pd.Timedelta(days=i+1)
        taux = float(forecast.iloc[i]["yhat"]) if hasattr(forecast, 'iloc') else float(forecast[i])
        predictions.append({
            "day": i+1,
            "predicted_value": taux,
            "date": pred_date.isoformat()
        })
    
    output = {
        "country": prediction_in.country,
        "prediction_type": "taux_mortalite",
        "days": prediction_in.days,
        "predictions": predictions
    }
    logger.info(f"[PREDICT] Output: {output}")
    return output

# Endpoint pour l'historique des prédictions
@router.get("/predictions/history", response_model=List[dict])
def get_prediction_history(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    """Récupère l'historique des prédictions de l'utilisateur."""
    # Pour l'instant, retourner une liste vide (à implémenter avec un modèle PredictionHistory)
    return []

# Endpoint pour recharger dynamiquement le modèle IA
@router.post("/reload")
def reload_model(
    current_user: models.User = Depends(auth.get_current_user)
):
    """Recharge le modèle IA. Requiert des droits administrateur."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin rights required")
    ml_model.load_model()
    return {"status": "Model reloaded"} 