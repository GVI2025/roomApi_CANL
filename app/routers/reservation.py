from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.services import reservation as reservation_service
from app.schemas.reservation import ReservationRead

from app.database.database import get_db

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.get("/", response_model=List[ReservationRead])
def list_reservations(db: Session = Depends(get_db)):
    return reservation_service.get_reservations(db)