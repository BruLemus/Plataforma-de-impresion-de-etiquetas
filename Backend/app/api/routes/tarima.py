# app/routers/tarima_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.tarima import TarimaCreate, TarimaUpdate, TarimaResponse
from app.services.tarima_services import create_tarima, get_tarimas, get_tarima_by_id, update_tarima, delete_tarima

router = APIRouter()

@router.post("/", response_model=TarimaResponse)
def crear_tarima(tarima: TarimaCreate, db: Session = Depends(get_db), coordinador_id: int = None, practicante_id: int = None, coordinador_nombre: str = None, practicante_nombre: str = None):
    return create_tarima(db, tarima, coordinador_id, practicante_id, coordinador_nombre, practicante_nombre)

@router.get("/", response_model=List[TarimaResponse])
def listar_tarimas(db: Session = Depends(get_db)):
    return get_tarimas(db)

@router.get("/{tarima_id}", response_model=TarimaResponse)
def obtener_tarima(tarima_id: int, db: Session = Depends(get_db)):
    tarima = get_tarima_by_id(db, tarima_id)
    if not tarima:
        raise HTTPException(status_code=404, detail="Tarima no encontrada")
    return tarima

@router.put("/{tarima_id}", response_model=TarimaResponse)
def editar_tarima(tarima_id: int, tarima_data: TarimaUpdate, db: Session = Depends(get_db)):
    tarima = update_tarima(db, tarima_id, tarima_data)
    if not tarima:
        raise HTTPException(status_code=404, detail="Tarima no encontrada")
    return tarima

@router.delete("/{tarima_id}")
def eliminar_tarima(tarima_id: int, db: Session = Depends(get_db)):
    if not delete_tarima(db, tarima_id):
        raise HTTPException(status_code=404, detail="Tarima no encontrada")
    return {"mensaje": "Tarima eliminada correctamente"}
