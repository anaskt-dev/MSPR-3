from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import schemas
import models
import database
import auth
from typing import List, Optional
import logging
import ml_model
import datetime
import data_loader

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

# Authentification


@router.post("/register", response_model=schemas.UserOut)
def register(
    user: schemas.UserCreate,  # Reçoit les données de l'utilisateur à créer, validées par le schéma UserCreate.
    db: Session = Depends(database.get_db)  # Injecte une session de base de données.
):
    """Enregistre un nouvel utilisateur dans la base de données.
    Vérifie si le nom d'utilisateur ou l'email existe déjà pour éviter les doublons.
    Hache le mot de passe avant de sauvegarder l'utilisateur."""
    # Vérifie si un utilisateur avec le même nom d'utilisateur ou email existe déjà.
    db_user = db.query(
        models.User).filter(
        (models.User.username == user.username) | (
            models.User.email == user.email)).first()
    if db_user:
        # Lève une exception HTTP 400 si l'utilisateur existe déjà.
        raise HTTPException(status_code=400, detail="Username or email already registered")

    # Hache le mot de passe avant de le stocker dans la base de données.
    hashed_password = auth.get_password_hash(user.password)
    # Crée une nouvelle instance du modèle User avec les données fournies.
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        country=user.country,
        is_admin=False)

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
    """
    Récupère les informations de l'utilisateur actuellement authentifié.
    Cette route nécessite un jeton JWT valide.
    """
    return schemas.UserOut.from_orm(current_user)

# Données historiques


@router.post("/data", response_model=schemas.DataOut)
def add_data(
    data: schemas.DataIn,  # Données COVID-19 à ajouter, validées par le schéma DataIn.
    db: Session = Depends(database.get_db),  # Injecte une session de base de données.
    # Assure que seul un utilisateur authentifié peut ajouter des données.
    current_user: models.User = Depends(auth.get_current_user)
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
    country: Optional[str] = Query(None),  # Paramètre de requête facultatif pour filtrer les données par pays.
    skip: int = 0,  # Paramètre pour la pagination : nombre d'éléments à ignorer.
    limit: int = 10000,  # Paramètre pour la pagination : nombre maximal d'éléments à retourner.
    db: Session = Depends(database.get_db)  # Injecte une session de base de données.
):
    """Récupère les données historiques de la pandémie. Peut être filtré par pays et paginé.
    Accessible publiquement (pas de dépendance d'authentification)."""
    query = db.query(models.Data)
    if country:
        query = query.filter(models.Data.country == country)  # Applique le filtre par pays si spécifié.
    # Exécute la requête avec les paramètres de pagination et retourne tous les résultats.
    data = query.offset(skip).limit(limit).all()
    return [schemas.DataOut.from_orm(d) for d in data]

# Récupérer tous les pays uniques


@router.get("/countries", response_model=List[str])
def get_all_countries(
    db: Session = Depends(database.get_db)  # Injecte une session de base de données.
):
    """Récupère une liste de tous les pays uniques présents dans les données COVID-19.
    Les pays sont triés par ordre alphabétique. Accessible publiquement."""
    # Récupère les noms de pays distincts et les trie.
    countries = db.query(models.Data.country).distinct().order_by(models.Data.country).all()
    return [country[0] for country in countries]  # Retourne une liste de chaînes de caractères (noms de pays).

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
def get_data_by_id(
    id: int, db: Session = Depends(
        database.get_db), current_user: models.User = Depends(
            auth.get_current_user)):
    data = db.query(models.Data).filter(models.Data.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return schemas.DataOut.from_orm(data)


@router.put("/data/id/{id}", response_model=schemas.DataOut)
def update_data(
    id: int, update: dict, db: Session = Depends(
        database.get_db), current_user: models.User = Depends(
            auth.get_current_user)):
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
def delete_data(
    id: int, db: Session = Depends(
        database.get_db), current_user: models.User = Depends(
            auth.get_current_user)):
    data = db.query(models.Data).filter(models.Data.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    db.delete(data)
    db.commit()
    return {"detail": "Data deleted"}

# --- GET par pays (corrigé) ---


@router.get("/data/country/{country}", response_model=List[schemas.DataOut])
def get_data_by_country(
    country: str, db: Session = Depends(
        database.get_db), current_user: models.User = Depends(
            auth.get_current_user)):
    data = db.query(models.Data).filter(models.Data.country == country).all()
    if not data:
        raise HTTPException(status_code=404, detail="No data found for this country")
    return [schemas.DataOut.from_orm(d) for d in data]

# --- Correction du endpoint de prédiction ---


@router.post("/predict", response_model=schemas.PredictionOut)
def get_prediction(
    prediction_in: schemas.PredictionIn,  # Données d'entrée pour la prédiction, validées par PredictionIn.
    db: Session = Depends(database.get_db),  # Injecte une session de base de données.
    # Assure que seul un utilisateur authentifié peut demander une prédiction.
    current_user: models.User = Depends(auth.get_current_user)
):
    """Effectue une prédiction basée sur le modèle IA chargé dynamiquement."""
    # Validation stricte des paramètres
    if prediction_in.days is None or prediction_in.days <= 0 or prediction_in.days > 30:
        raise HTTPException(status_code=422, detail="Le nombre de jours doit être entre 1 et 30.")
    if prediction_in.prediction_type not in ["cases", "deaths", "recovered"]:
        raise HTTPException(
            status_code=422,
            detail="Invalid prediction_type. Must be 'cases', 'deaths', or 'recovered'")
    # Vérifier que le pays a des données historiques
    historical_data = db.query(
        models.Data).filter(
        models.Data.country == prediction_in.country).order_by(
            models.Data.date.desc()).all()
    if not historical_data:
        raise HTTPException(status_code=404, detail=f"No data found for {prediction_in.country} to make a prediction.")

    # Simuler des prédictions basées sur les données historiques
    predictions = []
    latest_data = historical_data[0]

    for day in range(1, prediction_in.days + 1):
        # Simulation simple basée sur les tendances historiques
        if prediction_in.prediction_type == "cases":
            predicted_value = latest_data.confirmed + (latest_data.new_cases or 0) * day
        elif prediction_in.prediction_type == "deaths":
            predicted_value = latest_data.deaths + (latest_data.new_deaths or 0) * day
        elif prediction_in.prediction_type == "recovered":
            predicted_value = latest_data.recovered + (latest_data.new_recovered or 0) * day
        predictions.append({
            "day": day,
            "predicted_value": max(0, predicted_value),
            "date": latest_data.date + datetime.timedelta(days=day)
        })

    return schemas.PredictionOut(
        country=prediction_in.country,
        prediction_type=prediction_in.prediction_type,
        days=prediction_in.days,
        predictions=predictions
    )

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
