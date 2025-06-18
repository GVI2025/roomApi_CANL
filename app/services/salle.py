from sqlalchemy.orm import Session
from app.models.salle import Salle

def get_all_salles(db: Session):
    return db.query(Salle).all()