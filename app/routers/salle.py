from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.salle import SalleRead, SalleCreate, Salle
from app.services.salle import get_all_salles, create_salle
from app.database.database import get_db

router = APIRouter(prefix="/salles", tags=["Salles"])

@router.get("/", response_model=List[SalleRead])
def list_salles(db: Session = Depends(get_db)):
    return get_all_salles(db)

@router.post("/", response_model=Salle)
def create_new_salle(salle: SalleCreate, db: Session = Depends(get_db)):
    try:
        return create_salle(db, salle)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(ve)
        )
    except RuntimeError as re:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(re)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur inconnue lors de la création de la salle."
        )
