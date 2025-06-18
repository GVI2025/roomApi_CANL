import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

@pytest.fixture
def salle_payload():
    return {
        "nom": "Salle Test",
        "capacite": 40,
        "localisation": "Bâtiment Test"
    }

def test_create_salle_success(salle_payload):
    mock_salle = {
        "id": "fake-id",
        "nom": salle_payload["nom"],
        "capacite": salle_payload["capacite"],
        "localisation": salle_payload["localisation"]
    }
    with patch("app.routers.salle.create_salle", return_value=mock_salle):
        response = client.post("/salles/", json=salle_payload)
        assert response.status_code in (200, 201)
        data = response.json()
        assert data["nom"] == salle_payload["nom"]
        assert data["capacite"] == salle_payload["capacite"]
        assert data["localisation"] == salle_payload["localisation"]
        assert "id" in data

def test_create_salle_conflict(salle_payload):
    with patch("app.routers.salle.create_salle", side_effect=ValueError("Une salle avec ce nom existe déjà.")):
        response = client.post("/salles/", json=salle_payload)
        assert response.status_code == 409
        assert "existe déjà" in response.json()["detail"]

def test_create_salle_invalid():
    payload = {
        "nom": "",
        "capacite": -5,
        "localisation": ""
    }
    response = client.post("/salles/", json=payload)
    assert response.status_code == 422

def test_list_salles_success():
    mock_salles = [
        {
            "id": "id1",
            "nom": "Salle A",
            "capacite": 50,
            "localisation": "Bâtiment A"
        },
        {
            "id": "id2",
            "nom": "Salle B",
            "capacite": 30,
            "localisation": "Bâtiment B"
        }
    ]
    with patch("app.routers.salle.get_all_salles", return_value=mock_salles):
        response = client.get("/salles/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["nom"] == "Salle A"
        assert data[1]["nom"] == "Salle B"

def test_list_salles_empty():
    with patch("app.routers.salle.get_all_salles", return_value=[]):
        response = client.get("/salles/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0