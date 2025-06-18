from pydantic import BaseModel

class SalleRead(BaseModel):
    id: str
    nom: str
    capacite: int | None = None
    localisation: str | None = None

    class Config:
        orm_mode = True