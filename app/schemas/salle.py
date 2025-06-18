from pydantic import BaseModel, constr, conint
from typing import Optional

class SalleBase(BaseModel):
    nom: constr(min_length=1)
    capacite: conint(gt=0)
    localisation: constr(min_length=1)

class SalleCreate(SalleBase):
    pass

class SalleUpdate(BaseModel):
    nom: Optional[constr(min_length=1)] = None
    capacite: Optional[conint(gt=0)] = None
    localisation: Optional[constr(min_length=1)] = None

class Salle(SalleBase):
    id: str

    class Config:
<<<<<<< Updated upstream
        from_attributes = True
=======
        from_attributes = True

>>>>>>> Stashed changes
