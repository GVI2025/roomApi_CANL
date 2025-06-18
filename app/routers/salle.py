from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

<<<<<<< Updated upstream
=======
from app.schemas.salle import SalleRead, SalleCreate, Salle, SalleUpdate
from app.services.salle import get_all_salles, create_salle, update_salle
>>>>>>> Stashed changes
from app.database.database import get_db
from app.schemas.salle import SalleCreate, Salle
from app.services.salle import create_salle

router = APIRouter(prefix="/salles", tags=["Salles"])

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