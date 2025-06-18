from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

router = APIRouter(prefix="/salles", tags=["Salles"])

