from datetime import date, time
from sqlalchemy import extract
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
    query = db.query(ReservationModel).filter(
        ReservationModel.salle_id == salle_id,
        ReservationModel.date == date,
        extract('hour', ReservationModel.heure) == heure.hour  # ignore les minutes
    ).first()
    return query

def get_reservation_by_id(db: Session, idReservation: str):
    return db.query(ReservationModel).filter(ReservationModel.id == idReservation).first()

def delete_reservation(db: Session, reservation: ReservationModel):
    db.delete(reservation)
    db.commit()