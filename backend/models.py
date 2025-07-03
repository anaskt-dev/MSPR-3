# backend/models.py

# Importe les types de colonnes de SQLAlchemy
# pour définir le schéma de la base de données.
from sqlalchemy import Column, Integer
from sqlalchemy import String, DateTime, Boolean, Date, ForeignKey
# Importe le module datetime pour gérer les dates et heures.
import datetime
from sqlalchemy.orm import relationship
import base

# Crée une instance de la base déclarative.
# Tous les modèles de la base de données hériteront de cette classe.
# Base = declarative_base()


# --- Modèle User (Utilisateurs) ---
# Représente la table 'users' dans la base de données.
class User(base.Base):
    # Définit le nom de la table dans la base de données.
    __tablename__ = "users"

    # Colonnes de la table 'users':
    # Clé primaire auto-incrémentée et indexée.
    id = Column(Integer, primary_key=True, index=True)
    # Nom d'utilisateur, doit être unique, indexé et non nul.
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)  # Mot de passe haché, non nul.
    email = Column(String, nullable=True)  # Email optionnel
    country = Column(String, nullable=True)  # Pays optionnel
    # Indique si l'utilisateur est un administrateur, par défaut False.
    is_admin = Column(Boolean, default=False)
    # Indique si l'utilisateur est un administrateur, par défaut False.
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    # Un utilisateur peut avoir plusieurs entrées de données
    data_entries = relationship("Data", back_populates="owner")


# --- Modèle Data (Données COVID-19) ---
# Représente la table 'data' dans la base de données,
# stockant les informations sur la pandémie.
class Data(base.Base):
    # Définit le nom de la table dans la base de données.
    __tablename__ = "data"

    # Colonnes de la table 'data':
    # Clé primaire auto-incrémentée et indexée.
    id = Column(Integer, primary_key=True, index=True)
    # Pays associé à la donnée, indexé pour des recherches rapides.
    country = Column(String, index=True)
    date = Column(Date)  # Date de l'enregistrement de la donnée.
    confirmed = Column(Integer)  # Nombre de cas confirmés.
    # Nombre de décès, avec une valeur par défaut de 0.
    deaths = Column(Integer, default=0)
    # Nombre de cas guéris, avec une valeur par défaut de 0.
    recovered = Column(Integer, default=0)
    # Nombre de nouveaux cas (calculé ou fourni),
    # avec une valeur par défaut de 0.
    new_cases = Column(Integer, default=0)
    # Nombre de nouveaux décès (calculé ou fourni),
    # avec une valeur par défaut de 0.
    new_deaths = Column(Integer, default=0)
    # Nombre de nouveaux cas guéris (calculé ou fourni),
    # avec une valeur par défaut de 0.
    new_recovered = Column(Integer, default=0)
    # Chaque entrée de donnée appartient à un utilisateur
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="data_entries")
