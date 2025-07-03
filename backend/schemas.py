from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

# --- Schémas pour les Utilisateurs ---


# UserBase: Schéma de base pour les utilisateurs,
# définissant les champs communs.
class UserBase(BaseModel):
    # Nom d'utilisateur (chaîne de caractères).
    username: str
    # Adresse email, validée comme un format d'email standard.
    email: Optional[EmailStr] = None
    # Pays de l'utilisateur.
    country: Optional[str] = None


# UserCreate: Schéma utilisé pour la création d'un
# nouvel utilisateur. Hérite de UserBase et ajoute
# le champ 'password'.
class UserCreate(UserBase):
    # Mot de passe en clair (sera haché avant stockage).
    password: str


# UserOut: Schéma pour la sortie (réponse)
# des informations utilisateur.
# Hérite de UserBase et ajoute des
# champs générés par le système.
class UserOut(UserBase):
    id: int  # ID unique de l'utilisateur.
    is_admin: bool  # Statut d'administrateur (booléen).
    # Date et heure de création du compte.
    created_at: datetime.datetime

    # Configuration interne de Pydantic pour
    # mapper les attributs des objets SQLAlchemy aux champs Pydantic.
    class Config:
        orm_mode = True

# --- Schémas pour les Données COVID-19 ---


# DataIn: Schéma pour l'entrée de données COVID-19
# (lors de l'ajout de nouvelles données).
class DataIn(BaseModel):
    date: datetime.date  # Date de l'enregistrement.
    country: str  # Pays concerné.
    confirmed: int  # Nombre de cas confirmés.
    deaths: Optional[int] = 0  # Nombre de décès.
    recovered: Optional[int] = 0  # Nombre de cas guéris.
    new_cases: Optional[int] = 0  # Nombre de nouveaux cas.
    new_deaths: Optional[int] = 0  # Nombre de nouveaux décès.
    new_recovered: Optional[int] = 0  # Nombre de nouveaux cas guéris.


# DataOut: Schéma pour la sortie (réponse) des données COVID-19.
# Hérite de DataIn et ajoute le champ 'id' généré par la base de données.
class DataOut(DataIn):
    id: int  # ID unique de l'entrée de données.

    # Configuration pour le mappage avec les attributs SQLAlchemy.
    class Config:
        orm_mode = True

# --- Schémas pour la Prédiction IA ---


# PredictionIn: Schéma pour l'entrée des paramètres de la prédiction IA.
class PredictionIn(BaseModel):
    country: str  # Pays pour lequel la prédiction est demandée.
    days: int  # Nombre de jours à prédire (1-30).
    # Type de prédiction: "cases", "deaths", ou "recovered".
    prediction_type: str
    model: Optional[str] = 'prophet'  # 'prophet' ou 'lstm'
    # Date de référence historique (format ISO)
    reference_date: Optional[str] = None


# PredictionOut: Schéma pour la sortie (réponse) de la prédiction IA.
class PredictionOut(BaseModel):
    country: str
    prediction_type: str
    days: int
    predictions: list


# Ancien schéma pour compatibilité (à supprimer plus tard)
class PredictionInOld(BaseModel):
    country: str  # Pays pour lequel la prédiction est demandée.
    future_date: datetime.date


class PredictionOutOld(BaseModel):
    predicted_cases: float
    predicted_deaths: float
    predicted_recovered: float
    confidence: float

# --- Schémas pour l'Authentification (Jetons) ---


# Token: Schéma pour la réponse d'un jeton d'accès après connexion.
class Token(BaseModel):
    access_token: str  # Le jeton d'accès JWT.
    token_type: str  # Le type de jeton (généralement "bearer").


# TokenData: Schéma pour les données contenues dans un jeton JWT.
class TokenData(BaseModel):
    # Le nom d'utilisateur stocké dans le jeton
    # (peut être nul si non présent).
    username: Optional[str] = None
