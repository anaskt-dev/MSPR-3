import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app
from backend.database import Base, get_db
from backend import models

# Créer une base de test en mémoire SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crée la DB et les tables pour chaque test
@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)

# Override la dépendance get_db pour utiliser la DB de test
@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_register_user(client):
    # Données de l'utilisateur à enregistrer
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "strongpassword",
        "country": "FR"
    }
    response = client.post("/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "hashed_password" not in data  # Assure que le hash ne ressort pas

def test_register_duplicate_user(client):
    user_data = {
        "username": "duplicateuser",
        "email": "duplicate@example.com",
        "password": "strongpassword",
        "country": "FR"
    }
    # Premier enregistrement ok
    response1 = client.post("/register", json=user_data)
    assert response1.status_code == 200

    # Deuxième enregistrement avec même username/email -> 400
    response2 = client.post("/register", json=user_data)
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Username or email already registered"
