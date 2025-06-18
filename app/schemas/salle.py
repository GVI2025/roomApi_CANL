from pydantic import BaseModel, constr, conint
from typing import Optional

class SalleBase(BaseModel):
    nom: constr(min_length=1)
    capacite: conint(gt=0)
    localisation: constr(min_length=1)
    disponible: bool = True
      
class SalleRead(BaseModel):
    id: str
    nom: str
    capacite: int | None = None
    localisation: str | None = None
    disponible: bool = True

    class Config:
        orm_mode = True

class SalleCreate(SalleBase):
    pass

class SalleUpdate(BaseModel):
    nom: Optional[constr(min_length=1)] = None
    capacite: Optional[conint(gt=0)] = None
    localisation: Optional[constr(min_length=1)] = None
    disponible: Optional[bool] = None

class Salle(SalleBase):
    id: str

    class Config:
        from_attributes = True
