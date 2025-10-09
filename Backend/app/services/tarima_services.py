# app/services/tarima_services.py
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models.tarima import Tarima
from app.schemas.tarima import TarimaCreate, TarimaUpdate

from datetime import datetime

def create_tarima(db: Session, tarima_data: TarimaCreate, coordinador_id: Optional[int] = None, practicante_id: Optional[int] = None, coordinador_nombre: Optional[str] = None, practicante_nombre: Optional[str] = None) -> Tarima:
    tarima = Tarima(
        numero_facturas=tarima_data.numero_facturas,
        numero_tarimas=tarima_data.numero_tarimas,
        tipo_embalaje=tarima_data.tipo_embalaje,
        paqueteria=tarima_data.paqueteria,
        clave_producto=tarima_data.clave_producto,
        cantidad_piezas=tarima_data.cantidad_piezas,
        ancho=tarima_data.ancho,
        largo=tarima_data.largo,
        alto=tarima_data.alto,
        peso=tarima_data.peso,
        peso_volumetrico=tarima_data.peso_volumetrico,
        coordinador_id=coordinador_id,
        practicante_id=practicante_id,
        coordinador_nombre=coordinador_nombre,
        practicante_nombre=practicante_nombre,
        fecha_creacion=datetime.now()
    )
    db.add(tarima)
    db.commit()
    db.refresh(tarima)
    return tarima

def get_tarimas(db: Session, skip: int = 0, limit: int = 100) -> List[Tarima]:
    return db.query(Tarima).offset(skip).limit(limit).all()

def get_tarima_by_id(db: Session, tarima_id: int) -> Optional[Tarima]:
    return db.query(Tarima).filter(Tarima.id == tarima_id).first()

def update_tarima(db: Session, tarima_id: int, tarima_data: TarimaUpdate) -> Optional[Tarima]:
    tarima = db.query(Tarima).filter(Tarima.id == tarima_id).first()
    if not tarima:
        return None
    for field, value in tarima_data.dict(exclude_unset=True).items():
        setattr(tarima, field, value)
    tarima.fecha_actualizacion = datetime.now()
    db.commit()
    db.refresh(tarima)
    return tarima

def delete_tarima(db: Session, tarima_id: int) -> bool:
    tarima = db.query(Tarima).filter(Tarima.id == tarima_id).first()
    if not tarima:
        return False
    db.delete(tarima)
    db.commit()
    return True
