from sqlalchemy import Column, String, Integer, UniqueConstraint, Boolean
from uuid import uuid4

from app.database.database import Base

class Salle(Base):
    __tablename__ = "salles"
    __table_args__ = (UniqueConstraint('nom', name='uq_salle_nom'),)

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    nom = Column(String, nullable=False)
    capacite = Column(Integer)
    localisation = Column(String)
    disponible = Column(Boolean, default=True)  # 1 pour disponible, 0 pour indisponible
