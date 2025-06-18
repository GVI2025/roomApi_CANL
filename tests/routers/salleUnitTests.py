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
        "localisation": "Bâtiment Test",
        "disponible": True
    }

def test_create_salle_success(salle_payload):
    mock_salle = {
        "id": "fake-id",
        "nom": salle_payload["nom"],
        "capacite": salle_payload["capacite"],
        "localisation": salle_payload["localisation"],
        "disponible": salle_payload["disponible"]
    }
    with patch("app.routers.salle.create_salle", return_value=mock_salle):
        response = client.post("/salles/", json=salle_payload)
        assert response.status_code in (200, 201)
        data = response.json()
        assert data["nom"] == salle_payload["nom"]
        assert data["capacite"] == salle_payload["capacite"]
        assert data["localisation"] == salle_payload["localisation"]
        assert data["disponible"] == salle_payload["disponible"]
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
            "localisation": "Bâtiment A",
            "disponible": True
        },
        {
            "id": "id2",
            "nom": "Salle B",
            "capacite": 30,
            "localisation": "Bâtiment B",
            "disponible": False
        }
    ]
    with patch("app.routers.salle.get_all_salles", return_value=mock_salles):
        response = client.get("/salles/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["nom"] == "Salle A"
        assert data[0]["disponible"] is True
        assert data[1]["nom"] == "Salle B"
        assert data[1]["disponible"] is False

def test_list_salles_empty():
    with patch("app.routers.salle.get_all_salles", return_value=[]):
        response = client.get("/salles/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

def test_delete_salle_success():
    salle_id = "fake-id"

    # Mock la fonction get_salle_by_id pour renvoyer un objet simulé
    mock_salle = MagicMock()
    with patch("app.routers.salle.get_salle_by_id", return_value=mock_salle), \
         patch("app.routers.salle.delete_salle") as mock_delete:
        response = client.delete(f"/salles/{salle_id}")
        assert response.status_code == 204
        # On vérifie seulement que le deuxième argument est bien mock_salle
        called_args = mock_delete.call_args[0]
        assert called_args[1] == mock_salle

def test_delete_salle_not_found():
    salle_id = "non-existent-id"

    # Mock get_salle_by_id pour renvoyer None (pas trouvé)
    with patch("app.routers.salle.get_salle_by_id", return_value=None):
        response = client.delete(f"/salles/{salle_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Salle non trouvée"

def test_patch_salle_success():
    salle_id = "id1"
    update_payload = {
        "nom": "Salle Modifiée",
        "capacite": 60,
        "localisation": "Bâtiment Modifié",
        "disponible": False
    }
    mock_salle = {
        "id": salle_id,
        "nom": update_payload["nom"],
        "capacite": update_payload["capacite"],
        "localisation": update_payload["localisation"],
        "disponible": update_payload["disponible"]
    }
    with patch("app.routers.salle.update_salle", return_value=mock_salle):
        response = client.patch(f"/salles/{salle_id}", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == salle_id
        assert data["nom"] == update_payload["nom"]
        assert data["capacite"] == update_payload["capacite"]
        assert data["localisation"] == update_payload["localisation"]
        assert data["disponible"] == update_payload["disponible"]

def test_patch_salle_not_found():
    salle_id = "notfound"
    update_payload = {
        "nom": "Salle Inexistante"
    }
    with patch("app.routers.salle.update_salle", side_effect=ValueError("Salle non trouvée.")):
        response = client.patch(f"/salles/{salle_id}", json=update_payload)
        assert response.status_code == 404
        assert "non trouvée" in response.json()["detail"]

def test_patch_salle_conflict():
    salle_id = "id1"
    update_payload = {
        "nom": "Salle Déjà Existante"
    }
    with patch("app.routers.salle.update_salle", side_effect=ValueError("Une salle avec ce nom existe déjà.")):
        response = client.patch(f"/salles/{salle_id}", json=update_payload)
        assert response.status_code == 409
        assert "existe déjà" in response.json()["detail"]

def test_patch_salle_invalid():
    salle_id = "id1"
    update_payload = {
        "nom": "",
        "capacite": -10
    }
    response = client.patch(f"/salles/{salle_id}", json=update_payload)
    assert response.status_code == 422
