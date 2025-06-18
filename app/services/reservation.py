from sqlalchemy.orm import Session
from app.models import Reservation as ReservationModel
from datetime import date, time
from sqlalchemy.orm import Session
from app.models.reservation import Reservation as ReservationModel
from app.schemas.reservation import ReservationCreate

def get_reservations(db: Session):
    return db.query(ReservationModel).all()

def create_reservation(db: Session, reservation: ReservationCreate):
    db_reservation = ReservationModel(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def check_before_reservation(db:Session, salle_id:str, date: date, heure: time):
    query = db.query(ReservationModel)
    query = (query.filter(ReservationModel.salle_id == salle_id)
                  .filter(ReservationModel.date == date)
                  .filter(ReservationModel.heure == heure)
                  .first())
    return query