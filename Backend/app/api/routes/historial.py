from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.historial import HistorialSchema
from app.services.historial_service import obtener_historial

router = APIRouter(prefix="/historial", tags=["Historial"])

@router.get("/", response_model=list[HistorialSchema])
def listar_historial(db: Session = Depends(get_db)):
    datos = obtener_historial(db)
    return datos
