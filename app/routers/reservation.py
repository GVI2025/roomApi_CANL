from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.services import reservation as reservation_service
from app.schemas.reservation import ReservationRead,ReservationCreate

from app.database.database import get_db



router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.get("/", response_model=List[ReservationRead])
def list_reservations(db: Session = Depends(get_db)):
    return reservation_service.get_reservations(db)

@router.post("/", response_model=ReservationRead)
def create_reservation(reservationModel: ReservationCreate, db: Session = Depends(get_db)):
    existing = reservation_service.check_before_reservation(db,reservationModel.salle_id,reservationModel.date,reservationModel.heure)
    if existing:
        raise HTTPException(status_code=400, detail="Reservation Impossible, Une réservation pour cette salle existe déjà")
    return reservation_service.create_reservation(db, reservationModel)

@router.delete("/{idReservation}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(idReservation: str, db: Session = Depends(get_db)):
    reservation = reservation_service.get_reservation_by_id(db, idReservation)
    if not reservation:
        raise HTTPException(status_code=404, detail="Réservation non trouvée")
    reservation_service.delete_reservation(db, reservation)
    return None  # 204 No Content ne retourne rien