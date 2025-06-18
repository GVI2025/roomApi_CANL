import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_list_reservations_success():
    mock_reservations = [
        {
            "id": "res1",
            "salle_id": "id1",
            "date": "2024-06-01",
            "heure": "09:00:00",
            "utilisateur": "user1",
            "commentaire": "Réunion importante"
        },
        {
            "id": "res2",
            "salle_id": "id2",
            "date": "2024-06-02",
            "heure": "11:00:00",
            "utilisateur": "user2",
            "commentaire": None
        }
    ]
    with patch("app.services.reservation.get_reservations", return_value=mock_reservations):
        response = client.get("/reservations/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["id"] == "res1"
        assert data[0]["commentaire"] == "Réunion importante"
        assert data[1]["id"] == "res2"
        assert data[1]["commentaire"] is None

def test_list_reservations_empty():
    with patch("app.services.reservation.get_reservations", return_value=[]):
        response = client.get("/reservations/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

def test_create_reservation_success():
    payload = {
        "salle_id": "id1",
        "utilisateur": "user1",
        "date": "2024-06-01",
        "heure": "09:00:00",
        "commentaire": "Réunion importante"
    }
    mock_reservation = {
        "id": "res1",
        **payload
    }
    with patch("app.services.reservation.check_before_reservation", return_value=None), \
         patch("app.services.reservation.create_reservation", return_value=mock_reservation):
        response = client.post("/reservations/", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "res1"
        assert data["salle_id"] == payload["salle_id"]
        assert data["utilisateur"] == payload["utilisateur"]
        assert data["date"] == payload["date"]
        assert data["heure"] == payload["heure"]
        assert data["commentaire"] == payload["commentaire"]

def test_create_reservation_conflict():
    payload = {
        "salle_id": "id1",
        "utilisateur": "user1",
        "date": "2024-06-01",
        "heure": "09:00:00",
        "commentaire": "Tentative double réservation"
    }
    with patch("app.services.reservation.check_before_reservation", return_value=True):
        response = client.post("/reservations/", json=payload)
        assert response.status_code == 400
        assert "Impossible" in response.json()["detail"]

def test_create_reservation_invalid():
    payload = {
        "salle_id": "",
        "utilisateur": "",
        "date": "invalid-date",
        "heure": "invalid-heure",
        "commentaire": "Texte"
    }
    response = client.post("/reservations/", json=payload)
    assert response.status_code == 422
