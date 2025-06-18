from app.database.database import SessionLocal
from app.models.salle import Salle
from app.models.reservation import Reservation

from datetime import time, date
from sqlalchemy.exc import IntegrityError

def seed():
    db = SessionLocal()
    try:
        # Nettoyage de la base (dans l'ordre inverse des dépendances)
        db.query(Reservation).delete()
        db.query(Salle).delete()
        db.commit()

        # === SALLES ===
        salles = [
            Salle(
                id='10d55c46-9840-43f0-8dc5-23f8453b16d6',
                nom='Cafet',
                capacite=30,
                localisation='RDC',
                disponible=True
            ),
            Salle(
                id='da3d5688-0748-4461-ab27-5932b707d18f',
                nom='IG104',
                capacite=20,
                localisation='1er etage',
                disponible=True
            ),
            Salle(
                id='620d48b8-48ac-4353-9fa6-be268263c56c',
                nom='IG202',
                capacite=20,
                localisation='2eme etage',
                disponible=False
            ),
            Salle(
                id='5382f5bb-3b3a-4c11-886b-c3264eb441c5',
                nom='IG305',
                capacite=30,
                localisation='3eme etage',
                disponible=True
            ),
            Salle(
                id='7a855ef8-ed39-4c8b-9cfa-6696e48a1aa7',
                nom='IG301',
                capacite=50,
                localisation='3eme etage',
                disponible=False
            )
        ]

        # === RESERVATIONS ===
        reservations = [
            Reservation(
                id='bcf0911b-152b-4bee-8fb7-cb3409c3f7fd',
                salle_id='7a855ef8-ed39-4c8b-9cfa-6696e48a1aa7',
                utilisateur='Nawel Merabet',
                date=date(2025, 6, 16),
                heure=time(14, 0),
            ),
            Reservation(
                id='22293383-e13b-4d27-8068-a04a332f9182',
                salle_id='620d48b8-48ac-4353-9fa6-be268263c56c',
                utilisateur='Lara Viseur',
                date=date(2025, 6, 17),
                heure=time(12, 0),
            ),
        ]

        # Ajout global
        db.add_all(salles + reservations)
        db.commit()
        print("Données de test insérées avec succès.")

    except IntegrityError as e:
        db.rollback()
        print("Erreur d'intégrité :", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed()