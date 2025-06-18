from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.reservation import ReservationCreate,ReservationRead
from app.services import reservation as reservation_service
from app.database.database import get_db

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.post("/", response_model=ReservationRead)
def create_reservation(reservationModel: ReservationCreate, db: Session = Depends(get_db)):
    existing = reservation_service.check_before_reservation(db,reservationModel.salle_id,reservationModel.date,reservationModel.heure)
    if existing:
        raise HTTPException(status_code=400, detail="Reservation Impossible, Une réservation pour cette salle existe déjà")
    return reservation_service.create_reservation(db, reservationModel)