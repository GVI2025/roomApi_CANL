from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.salle import Salle as SalleModel
from app.schemas.salle import SalleCreate, SalleUpdate

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

def update_salle(db: Session, salle_id: str, salle_update: SalleUpdate) -> SalleModel:
    db_salle = db.query(SalleModel).filter(SalleModel.id == salle_id).first()
    if not db_salle:
        raise ValueError("Salle non trouvée.")

    # Vérifier unicité du nom si modifié
    if salle_update.nom and salle_update.nom != db_salle.nom:
        existing = db.query(SalleModel).filter(SalleModel.nom == salle_update.nom).first()
        if existing:
            raise ValueError("Une salle avec ce nom existe déjà.")

    # Mise à jour des champs
    update_data = salle_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_salle, key, value)

    try:
        db.commit()
        db.refresh(db_salle)
        return db_salle
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError("Erreur lors de la modification de la salle.") from e