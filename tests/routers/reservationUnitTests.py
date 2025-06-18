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
            "utilisateur": "user1"
        },
        {
            "id": "res2",
            "salle_id": "id2",
            "date": "2024-06-02",
            "heure": "11:00:00",
            "utilisateur": "user2"
        }
    ]
    with patch("app.services.reservation.get_reservations", return_value=mock_reservations):
        response = client.get("/reservations/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["id"] == "res1"
        assert data[1]["id"] == "res2"

def test_list_reservations_empty():
    with patch("app.services.reservation.get_reservations", return_value=[]):
        response = client.get("/reservations/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
