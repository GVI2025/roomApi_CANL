from datetime import date, time
from sqlalchemy.orm import Session
from app.models.reservation import Reservation as ReservationModel
from app.schemas.reservation import ReservationCreate

def create_reservation(db: Session, reservation: ReservationCreate):
    db_reservation = ReservationModel(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def list_reservation(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ReservationModel).offset(skip).limit(limit).all()

def check_before_reservation(db:Session, salle_id:str, date: date, heure: time):
    query = db.query(ReservationModel)
    query = (query.filter(ReservationModel.salle_id == salle_id)
                  .filter(ReservationModel.date == date)
                  .filter(ReservationModel.heure == heure)
                  .first())
    return query