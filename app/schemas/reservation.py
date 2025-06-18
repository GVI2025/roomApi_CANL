from pydantic import BaseModel
from typing import Optional
from datetime import date, time

from sqlalchemy import Enum

class ReservationBase(BaseModel):
    salle_id: str
    utilisateur: str
    date: date
    heure: time
    commentaire: Optional[str] = None

class ReservationRead(ReservationBase):
    id: str

class ReservationStatus(str, Enum):
    LIBRE = "Salle Libre"
    RESERVE = "Salle Réservé"

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(ReservationBase):
    pass

    class Config:
        orm_mode = True
