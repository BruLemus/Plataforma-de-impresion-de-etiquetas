# app/services/caja_service.py
from sqlalchemy.orm import Session
from app.db.models.caja import Caja
from app.schemas.caja import CajaCreate
from typing import List, Optional

def create_caja(db: Session, caja: CajaCreate) -> Caja:
    # pydantic -> dict -> SQLAlchemy constructor (enum types are compatibles)
    db_caja = Caja(**caja.dict())
    db.add(db_caja)
    db.commit()
    db.refresh(db_caja)
    return db_caja

def get_cajas(db: Session, skip: int = 0, limit: int = 100, paqueteria: Optional[str] = None, numero_factura: Optional[str] = None) -> List[Caja]:
    query = db.query(Caja)
    if paqueteria:
        query = query.filter(Caja.paqueteria == paqueteria)
    if numero_factura:
        query = query.filter(Caja.numero_factura == numero_factura)
    return query.offset(skip).limit(limit).all()

def get_caja_by_id(db: Session, caja_id: int):
    return db.query(Caja).filter(Caja.id == caja_id).first()

def delete_caja(db: Session, caja_id: int) -> bool:
    db_caja = db.query(Caja).filter(Caja.id == caja_id).first()
    if db_caja:
        db.delete(db_caja)
        db.commit()
        return True
    return False

def update_caja(db: Session, caja_id: int, updated_data: dict) -> Optional[Caja]:
    db_caja = db.query(Caja).filter(Caja.id == caja_id).first()
    if db_caja:
        for key, value in updated_data.items():
            setattr(db_caja, key, value)
        db.commit()
        db.refresh(db_caja)
        return db_caja
    return None
