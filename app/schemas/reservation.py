from pydantic import BaseModel
from datetime import date, time

from sqlalchemy import Enum


class ReservationBase(BaseModel):
    salle_id: str
    utilisateur: str
    date: date
    heure: time

class ReservationRead(ReservationBase):
    id: str

    class Config:
        orm_mode = True


class ReservationStatus(str, Enum):
    LIBRE = "Salle Libre"
    RESERVE = "Salle Réservé"

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(ReservationBase):
    pass

