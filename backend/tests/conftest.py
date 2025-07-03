import sys
import os
import pytest
import main
import database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope="function")
def test_app():
    # Utilise une base SQLite temporaire sur disque
    test_db_path = "./test.db"
    engine = create_engine(f"sqlite:///{test_db_path}")
    TestingSessionLocal = sessionmaker(autocommit=False,
                                       autoflush=False, bind=engine)
    database.base.Base.metadata.create_all(bind=engine)
    main.app.dependency_overrides = {}

    # Patch la dépendance get_db pour utiliser la base de test
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    main.app.dependency_overrides[database.get_db] = override_get_db
    yield main.app
    main.app.dependency_overrides = {}
    # Nettoyage : supprime le fichier de base de test
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
