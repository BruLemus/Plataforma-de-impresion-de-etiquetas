from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from app.schemas.tarima import TarimaCreate, TarimaRead
from app.services import tarima_services
from app.db.database import get_db
from app.core.security import get_current_user  # Devuelve UserCoordinador o UserPracticante

router = APIRouter(prefix="/tarimas", tags=["Tarimas"])


# -----------------------------
# CREAR TARIMA
# -----------------------------
@router.post("/", response_model=TarimaRead)
def create_tarima_endpoint(
    payload: TarimaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Crea una tarima asignando automáticamente coordinador o practicante
    según el usuario logueado.
    """
    return tarima_services.create_tarima(db, payload, current_user)


# -----------------------------
# LISTAR TARIMAS CON FILTROS OPCIONALES
# -----------------------------
@router.get("/", response_model=List[TarimaRead])
def list_tarimas(
    skip: int = 0,
    limit: int = 100,
    paqueteria: Optional[str] = None,
    numero_factura: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Lista tarimas, opcionalmente filtradas por paquetería, número de factura
    y usuario logueado (coordinador/practicante).
    """
    return tarima_services.get_tarimas(
        db,
        skip=skip,
        limit=limit,
        paqueteria=paqueteria,
        numero_factura=numero_factura,
        current_user=current_user
    )


# -----------------------------
# OBTENER TARIMA POR ID
# -----------------------------
@router.get("/{tarima_id}", response_model=TarimaRead)
def get_tarima(tarima_id: int, db: Session = Depends(get_db)):
    db_tarima = tarima_services.get_tarima_by_id(db, tarima_id)
    if not db_tarima:
        raise HTTPException(status_code=404, detail="Tarima no encontrada")
    return db_tarima


# -----------------------------
# ACTUALIZAR TARIMA
# -----------------------------
@router.put("/{tarima_id}", response_model=TarimaRead)
def update_tarima_endpoint(
    tarima_id: int,
    payload: TarimaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Actualiza una tarima. 
    (No cambia automáticamente el usuario creador).
    """
    db_tarima = tarima_services.update_tarima(db, tarima_id, payload)
    if not db_tarima:
        raise HTTPException(status_code=404, detail="Tarima no encontrada")
    return db_tarima


# -----------------------------
# ELIMINAR TARIMA
# -----------------------------
@router.delete("/{tarima_id}")
def delete_tarima_endpoint(tarima_id: int, db: Session = Depends(get_db)):
    deleted = tarima_services.delete_tarima(db, tarima_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tarima no encontrada")
    return {"detail": "Tarima eliminada correctamente"}
