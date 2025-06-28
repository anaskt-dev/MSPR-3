# backend/models.py

# Importe les types de colonnes de SQLAlchemy pour définir le schéma de la base de données.
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Date, ForeignKey
# Importe `declarative_base` pour créer une classe de base déclarative pour les modèles SQLAlchemy.
from sqlalchemy.ext.declarative import declarative_base
# Importe le module datetime pour gérer les dates et heures.
import datetime
from sqlalchemy.orm import relationship
from base import Base

# Crée une instance de la base déclarative. Tous les modèles de la base de données hériteront de cette classe.
# Base = declarative_base()

# --- Modèle User (Utilisateurs) ---
# Représente la table 'users' dans la base de données.
class User(Base):
    __tablename__ = "users" # Définit le nom de la table dans la base de données.

    # Colonnes de la table 'users':
    id = Column(Integer, primary_key=True, index=True) # Clé primaire auto-incrémentée et indexée.
    username = Column(String, unique=True, index=True) # Nom d'utilisateur, doit être unique, indexé et non nul.
    hashed_password = Column(String) # Mot de passe haché, non nul.
    email = Column(String, nullable=True) # Email optionnel
    country = Column(String, nullable=True) # Pays optionnel
    is_admin = Column(Boolean, default=False) # Indique si l'utilisateur est un administrateur, par défaut False.
    created_at = Column(DateTime, default=datetime.datetime.utcnow) # Date de création du compte
    # Un utilisateur peut avoir plusieurs entrées de données
    data_entries = relationship("Data", back_populates="owner")

# --- Modèle Data (Données COVID-19) ---
# Représente la table 'data' dans la base de données, stockant les informations sur la pandémie.
class Data(Base):
    __tablename__ = "data" # Définit le nom de la table dans la base de données.

    # Colonnes de la table 'data':
    id = Column(Integer, primary_key=True, index=True) # Clé primaire auto-incrémentée et indexée.
    country = Column(String, index=True) # Pays associé à la donnée, indexé pour des recherches rapides.
    date = Column(Date) # Date de l'enregistrement de la donnée.
    confirmed = Column(Integer) # Nombre de cas confirmés.
    deaths = Column(Integer, default=0) # Nombre de décès, avec une valeur par défaut de 0.
    recovered = Column(Integer, default=0) # Nombre de cas guéris, avec une valeur par défaut de 0.
    new_cases = Column(Integer, default=0) # Nombre de nouveaux cas (calculé ou fourni), avec une valeur par défaut de 0.
    new_deaths = Column(Integer, default=0) # Nombre de nouveaux décès (calculé ou fourni), avec une valeur par défaut de 0.
    new_recovered = Column(Integer, default=0) # Nombre de nouveaux cas guéris (calculé ou fourni), avec une valeur par défaut de 0.
    # Chaque entrée de donnée appartient à un utilisateur
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="data_entries") 