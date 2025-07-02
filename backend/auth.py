from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import models
import schemas
import database
from sqlalchemy.orm import Session
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Configuration de la sécurité
# ATTENTION: En production, cette clé secrète doit être une valeur forte
# et chargée depuis une variable d'environnement ou un service de gestion des secrets.
# Ne jamais la laisser en dur dans le code source pour des raisons de
# sécurité !
SECRET_KEY = "secret-key-change-me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme (tokenUrl doit correspondre à la route de login dans FastAPI)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


def verify_password(plain_password, hashed_password):
    """Vérifie si un mot de passe en clair correspond à un mot de passe haché."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Hache un mot de passe en clair."""
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    """Récupère un utilisateur de la base de données par son nom d'utilisateur."""
    return db.query(models.User).filter(models.User.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    """Authentifie un utilisateur en vérifiant son nom d'utilisateur et son mot de passe.
    Retourne l'objet utilisateur si l'authentification réussit, False sinon."""
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crée un jeton d'accès JWT avec les données fournies et une date d'expiration."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Expiration par défaut si non spécifiée.
        expire = datetime.utcnow() + timedelta(minutes=15)
    # Ajoute la date d'expiration au payload du jeton.
    to_encode.update({"exp": expire})
    # Encode le JWT.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """Récupère et valide l'utilisateur courant à partir du jeton d'authentification fourni."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Log le jeton reçu (à des fins de débogage).
        logger.debug(f"Received token: {token}")
        # Décode le jeton JWT en utilisant la clé secrète et l'algorithme
        # spécifié.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Extrait le nom d'utilisateur du payload.
        username: str = payload.get("sub")
        if username is None:
            # Log l'erreur si le nom d'utilisateur est absent.
            logger.error("Username is None in token payload")
            raise credentials_exception
        # Log le nom d'utilisateur décodé.
        logger.debug(f"Decoded username from token: {username}")
    except JWTError as e:
        # Log les erreurs de décodage JWT.
        logger.error(f"JWT decode error: {str(e)}")
        raise credentials_exception

    # Tente de récupérer l'utilisateur de la base de données en utilisant le
    # nom d'utilisateur extrait.
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        # Log l'erreur si l'utilisateur n'est pas trouvé.
        logger.error(f"User not found for username: {username}")
        raise credentials_exception
    logger.debug(f"Found user: {user.username}")  # Log l'utilisateur trouvé.
    return user  # Retourne l'objet utilisateur.


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)
):
    """Endpoint pour la connexion des utilisateurs et la génération d'un jeton d'accès JWT."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        # Lève une exception HTTP 401 si l'authentification échoue.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Calcule la durée d'expiration du jeton.
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Crée le jeton d'accès avec le nom d'utilisateur comme sujet (sub).
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    # Retourne le jeton d'accès et son type (bearer).
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """Endpoint alternatif pour la connexion (alias de /token)."""
    return await login_for_access_token(form_data, db)


@router.get("/users/me", response_model=schemas.UserOut)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    """Endpoint pour récupérer les informations de l'utilisateur connecté."""
    return current_user
