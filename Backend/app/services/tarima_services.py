from sqlalchemy.orm import Session
from app.db.models.tarima import Tarima
from app.schemas.tarima import TarimaCreate
from typing import List, Optional

# -----------------------------
# CREAR TARIMA CON USUARIO LOGUEADO
# -----------------------------
def create_tarima(db: Session, payload: TarimaCreate, current_user: dict):
    """
    current_user: dict con {'tipo': 'coordinador' o 'practicante', 'id': <int>}
    """
    db_tarima = Tarima(**payload.dict())

    # Asignar automáticamente según quien esté logueado
    if current_user["tipo"] == "coordinador":
        db_tarima.coordinador_id = current_user["id"]
    elif current_user["tipo"] == "practicante":
        db_tarima.practicante_id = current_user["id"]

    db.add(db_tarima)
    db.commit()
    db.refresh(db_tarima)
    return db_tarima

# -----------------------------
# OBTENER TARIMAS
# -----------------------------
def get_tarimas(db: Session, skip: int = 0, limit: int = 100, paqueteria: str = None, numero_factura: str = None):
    query = db.query(Tarima)
    if paqueteria:
        query = query.filter(Tarima.paqueteria == paqueteria)
    if numero_factura:
        query = query.filter(Tarima.numero_factura == numero_factura)
    return query.offset(skip).limit(limit).all()

# -----------------------------
# OBTENER TARIMA POR ID
# -----------------------------
def get_tarima_by_id(db: Session, tarima_id: int):
    return db.query(Tarima).filter(Tarima.tarima_id == tarima_id).first()

# -----------------------------
# ACTUALIZAR TARIMA
# -----------------------------
def update_tarima(db: Session, tarima_id: int, payload: TarimaCreate):
    db_tarima = get_tarima_by_id(db, tarima_id)
    if not db_tarima:
        return None
    for key, value in payload.dict().items():
        setattr(db_tarima, key, value)
    db.commit()
    db.refresh(db_tarima)
    return db_tarima

# -----------------------------
# ELIMINAR TARIMA
# -----------------------------
def delete_tarima(db: Session, tarima_id: int):
    db_tarima = get_tarima_by_id(db, tarima_id)
    if not db_tarima:
        return False
    db.delete(db_tarima)
    db.commit()
    return True
