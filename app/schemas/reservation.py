from pydantic import BaseModel
from datetime import date,time
from enum import Enum

class ReservationStatus(str, Enum):
    LIBRE = "Salle Libre"
    RESERVE = "Salle Réservé"

class ReservationBase(BaseModel):
    salle_id : str
    utilisateur : str
    date : date
    heure : time

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(ReservationBase):
    pass

class ReservationRead(ReservationBase):
    id: str

    class Config:
        orm_mode = True
