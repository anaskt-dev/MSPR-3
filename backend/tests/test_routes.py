import models
from fastapi.testclient import TestClient
from datetime import date


def test_get_countries(test_app):
    client = TestClient(test_app)
    # Insère un pays de test
    override = list(test_app.dependency_overrides.values())[0]
    db = next(override())
    db.add(models.Data(country="TestLand", date=date(2020, 1, 1), confirmed=1))
    db.commit()
    db.close()

    response = client.get("/api/countries")
    assert response.status_code == 200
    assert "TestLand" in response.json()
