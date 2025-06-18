from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.salle import SalleRead, SalleCreate, Salle, SalleUpdate
from app.services.salle import get_all_salles, create_salle, update_salle

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

@router.patch("/{idSalle}", response_model=Salle)
def patch_salle(idSalle: str, salle_update: SalleUpdate, db: Session = Depends(get_db)):
    try:
        return update_salle(db, idSalle, salle_update)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "non trouvée" in str(ve) else status.HTTP_409_CONFLICT,
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
            detail="Erreur inconnue lors de la modification de la salle."
        )