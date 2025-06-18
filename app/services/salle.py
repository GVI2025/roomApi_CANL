from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.salle import Salle as SalleModel
from app.schemas.salle import SalleCreate

def get_all_salles(db: Session):
    return db.query(SalleModel).all()

def create_salle(db: Session, salle: SalleCreate) -> SalleModel:
    # Vérifier si une salle avec le même nom existe déjà
    existing = db.query(SalleModel).filter(SalleModel.nom == salle.nom).first()
    if existing:
        raise ValueError("Une salle avec ce nom existe déjà.")

    db_salle = SalleModel(
        nom=salle.nom,
        capacite=salle.capacite,
        localisation=salle.localisation
    )
    try:
        db.add(db_salle)
        db.commit()
        db.refresh(db_salle)
        return db_salle
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError("Erreur lors de la création de la salle.") from e

def get_salle_by_id(db: Session, salle_id: str):
    return db.query(SalleModel).filter(SalleModel.id == salle_id).first()

def delete_salle(db: Session, salle: SalleModel):
    db.delete(salle)
    db.commit()