from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.database import get_db
from app.db.models.caja import Caja
from app.db.models.enums import PaqueteriaEnum, TipoEmbalajeEnum
from app.db.models.tarima import Tarima, PaqueteriaEnum as TarimaPaqueteriaEnum, TipoEmbalajeEnum as TarimaTipoEmbalajeEnum
from app.db.models.user_coordinador import UserCoordinador
from app.db.models.user_practicante import UserPracticante
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# ----------------------
# GET: Listar historial
# ----------------------
@router.get("/")
def get_historial(db: Session = Depends(get_db)):
    result = []

    # Traer todas las cajas con sus usuarios
    cajas = db.query(Caja).all()
    for c in cajas:
        usuario = "Desconocido"
        if c.coordinador:
            usuario = c.coordinador.nombre
        elif c.practicante:
            usuario = c.practicante.nombre

        result.append({
            "id": c.id,
            "numero_factura": c.numero_factura,
            "paqueteria": c.paqueteria.value if c.paqueteria else None,
            "cantidad_piezas": c.cantidad_piezas,
            "clave_producto": c.clave_producto,
            "tipo_embalaje": c.tipo_embalaje.value if c.tipo_embalaje else None,
            "fecha_creacion": c.fecha_creacion,
            "tipo_pedido": "Caja",
            "usuario": usuario
        })

    # Traer todas las tarimas con sus usuarios
    tarimas = db.query(Tarima).all()
    for t in tarimas:
        usuario = "Desconocido"
        if t.coordinador:
            usuario = t.coordinador.nombre
        elif t.practicante:
            usuario = t.practicante.nombre

        result.append({
            "id": t.tarima_id,
            "numero_factura": t.numero_factura,
            "paqueteria": t.paqueteria.value if t.paqueteria else None,
            "cantidad_piezas": t.cantidad_piezas,
            "clave_producto": t.clave_producto,
            "tipo_embalaje": t.tipo_embalaje.value if t.tipo_embalaje else None,
            "fecha_creacion": t.fecha_creacion,
            "tipo_pedido": "Tarima",
            "usuario": usuario
        })

    # Ordenar por fecha
    result.sort(key=lambda x: x["fecha_creacion"])
    return result

# ----------------------
# DELETE: Eliminar registros
# ----------------------
@router.delete("/caja/{caja_id}")
def eliminar_caja(caja_id: int, db: Session = Depends(get_db)):
    caja = db.query(Caja).filter(Caja.id == caja_id).first()
    if not caja:
        raise HTTPException(status_code=404, detail="Caja no encontrada")
    db.delete(caja)
    db.commit()
    return {"mensaje": "Caja eliminada correctamente"}

@router.delete("/tarima/{tarima_id}")
def eliminar_tarima(tarima_id: int, db: Session = Depends(get_db)):
    tarima = db.query(Tarima).filter(Tarima.tarima_id == tarima_id).first()
    if not tarima:
        raise HTTPException(status_code=404, detail="Tarima no encontrada")
    db.delete(tarima)
    db.commit()
    return {"mensaje": "Tarima eliminada correctamente"}

# ----------------------
# PUT: Editar registros con validación ENUM
# ----------------------
class CajaUpdate(BaseModel):
    numero_factura: Optional[str]
    paqueteria: Optional[str]
    cantidad_piezas: Optional[int]
    clave_producto: Optional[str]
    tipo_embalaje: Optional[int]

@router.put("/caja/{caja_id}")
def editar_caja(caja_id: int, data: CajaUpdate, db: Session = Depends(get_db)):
    caja = db.query(Caja).filter(Caja.id == caja_id).first()
    if not caja:
        raise HTTPException(status_code=404, detail="Caja no encontrada")

    # Validar ENUMs
    if data.paqueteria:
        try:
            caja.paqueteria = PaqueteriaEnum(data.paqueteria)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Paqueteria inválida. Valores permitidos: {[e.value for e in PaqueteriaEnum]}"
            )

    if data.tipo_embalaje:
        try:
            caja.tipo_embalaje = TipoEmbalajeEnum(data.tipo_embalaje)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de embalaje inválido. Valores permitidos: {[e.value for e in TipoEmbalajeEnum]}"
            )

    # Asignar el resto de campos
    for field, value in data.dict(exclude_unset=True).items():
        if field not in ["paqueteria", "tipo_embalaje"]:
            setattr(caja, field, value)

    caja.fecha_actualizacion = datetime.now()
    db.commit()
    db.refresh(caja)
    return {"mensaje": "Caja actualizada", "caja": caja}

class TarimaUpdate(BaseModel):
    numero_factura: Optional[str]
    paqueteria: Optional[str]
    cantidad_piezas: Optional[int]
    clave_producto: Optional[str]
    tipo_embalaje: Optional[int]

@router.put("/tarima/{tarima_id}")
def editar_tarima(tarima_id: int, data: TarimaUpdate, db: Session = Depends(get_db)):
    tarima = db.query(Tarima).filter(Tarima.tarima_id == tarima_id).first()
    if not tarima:
        raise HTTPException(status_code=404, detail="Tarima no encontrada")

    # Validar ENUMs
    if data.paqueteria:
        try:
            tarima.paqueteria = TarimaPaqueteriaEnum(data.paqueteria)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Paqueteria inválida. Valores permitidos: {[e.value for e in TarimaPaqueteriaEnum]}"
            )

    if data.tipo_embalaje:
        try:
            tarima.tipo_embalaje = TarimaTipoEmbalajeEnum(data.tipo_embalaje)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de embalaje inválido. Valores permitidos: {[e.value for e in TarimaTipoEmbalajeEnum]}"
            )

    # Asignar el resto de campos
    for field, value in data.dict(exclude_unset=True).items():
        if field not in ["paqueteria", "tipo_embalaje"]:
            setattr(tarima, field, value)

    tarima.fecha_actualizacion = datetime.now()
    db.commit()
    db.refresh(tarima)
    return {"mensaje": "Tarima actualizada", "tarima": tarima}
