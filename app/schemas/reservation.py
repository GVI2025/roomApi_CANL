from pydantic import BaseModel
from datetime import date, time

class ReservationBase(BaseModel):
    salle_id: str
    utilisateur: str
    date: date
    heure: time

class ReservationRead(ReservationBase):
    id: str

    class Config:
        orm_mode = True