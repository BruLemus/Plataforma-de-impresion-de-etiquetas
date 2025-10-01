from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.caja import CajaCreate, CajaRead
from typing import Optional, List
from app.services import caja_service
from app.db.database import get_db



router = APIRouter()




# ✅ Crear caja
@router.post("/", response_model=CajaRead)
def create_caja_endpoint(payload: CajaCreate, db: Session = Depends(get_db)):
    return caja_service.create_caja(db, payload)


# ✅ Listar cajas con filtros opcionales
@router.get("/", response_model=List[CajaRead])
def list_cajas(
    skip: int = 0,
    limit: int = 100,
    paqueteria: Optional[str] = None,
    numero_factura: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return caja_service.get_cajas(db, skip=skip, limit=limit, paqueteria=paqueteria, numero_factura=numero_factura)


# ✅ Obtener caja por ID
@router.get("/{caja_id}", response_model=CajaRead)
def get_caja(caja_id: int, db: Session = Depends(get_db)):
    db_caja = caja_service.get_caja_by_id(db, caja_id)
    if not db_caja:
        raise HTTPException(status_code=404, detail="Caja no encontrada")
    return db_caja


# ✅ Actualizar caja
@router.put("/{caja_id}", response_model=CajaRead)
def update_caja(caja_id: int, payload: CajaCreate, db: Session = Depends(get_db)):
    db_caja = caja_service.update_caja(db, caja_id, payload)
    if not db_caja:
        raise HTTPException(status_code=404, detail="Caja no encontrada")
    return db_caja


# ✅ Eliminar caja
@router.delete("/{caja_id}")
def delete_caja(caja_id: int, db: Session = Depends(get_db)):
    deleted = caja_service.delete_caja(db, caja_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Caja no encontrada")
    return {"detail": "Caja eliminada correctamente"}
