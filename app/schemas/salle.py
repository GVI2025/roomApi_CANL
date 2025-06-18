from pydantic import BaseModel, constr, conint

class SalleBase(BaseModel):
    nom: constr(min_length=1)
    capacite: conint(gt=0)
    localisation: constr(min_length=1)

class SalleCreate(SalleBase):
    pass

class Salle(SalleBase):
    id: str

    class Config:
        from_attributes = True