from sqlalchemy.orm import Session
from app.models import Reservation as ReservationModel
from app.models.reservation import Reservation
def get_reservations(db: Session):
    return db.query(ReservationModel).all()