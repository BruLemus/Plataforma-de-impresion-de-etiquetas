from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.db.database import get_db
from app.db.models.caja import Caja
from app.db.models.tarima import Tarima
from app.db.models.enums import PaqueteriaEnum, TipoEmbalajeEnum
from pydantic import BaseModel

router = APIRouter(prefix="/registros", tags=["Registros"])

# ------------------------------------------------------------------
# ✅ GET: Obtener todos los registros (Cajas y Tarimas)
# ------------------------------------------------------------------
@router.get("/")
def obtener_registros(db: Session = Depends(get_db)):
    registros = []

    # 🔹 Obtener cajas
    cajas = db.query(Caja).all()
    for c in cajas:
        usuario = c.nombre_user_coordinador or c.nombre_user_practicante or "Desconocido"
        registros.append({
            "id": c.id,
            "nombre_usuario": usuario,
            "factura": c.n_facturas,
            "cantidad": c.cantidad_piezas,
            "tipo_embalaje": c.t_embalaje.value if c.t_embalaje else None,
            "paqueteria": c.paqueteria.value if c.paqueteria else None,
            "clave_producto": c.clave_producto,
            "tipo_pedido": "Caja",
            "fecha_creacion": c.fecha_hora,
            "largo": c.largo,
            "ancho": c.ancho,
            "alto": c.alto,
            "peso": c.peso,
            "peso_volumetrico": c.peso_volumetrico
        })

    # 🔹 Obtener tarimas
    tarimas = db.query(Tarima).all()
    for t in tarimas:
        usuario = t.nombre_user_coordinador or t.nombre_user_practicante or "Desconocido"
        registros.append({
            "id": t.id,
            "nombre_usuario": usuario,
            "factura": t.numero_facturas,
            "cantidad": t.cantidad_piezas,
            "tipo_embalaje": t.tipo_embalaje.value if t.tipo_embalaje else None,
            "paqueteria": t.paqueteria.value if t.paqueteria else None,
            "clave_producto": t.clave_producto,
            "tipo_pedido": "Tarima",
            "fecha_creacion": t.fecha_hora,
            "largo": t.largo,
            "ancho": t.ancho,
            "alto": t.alto,
            "peso": t.peso,
            "peso_volumetrico": t.peso_volumetrico
        })

    # Ordenar por fecha más reciente
    registros.sort(key=lambda x: x["fecha_creacion"], reverse=True)
    return registros

# ------------------------------------------------------------------
# 🗑️ DELETE: Eliminar Caja o Tarima
# ------------------------------------------------------------------
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
    tarima = db.query(Tarima).filter(Tarima.id == tarima_id).first()
    if not tarima:
        raise HTTPException(status_code=404, detail="Tarima no encontrada")
    db.delete(tarima)
    db.commit()
    return {"mensaje": "Tarima eliminada correctamente"}

# ------------------------------------------------------------------
# ✏️ PUT: Editar Caja
# ------------------------------------------------------------------
class CajaUpdate(BaseModel):
    numero_factura: Optional[str]
    paqueteria: Optional[str]
    cantidad_piezas: Optional[int]
    clave_producto: Optional[str]
    tipo_embalaje: Optional[str]
    largo: Optional[float]
    ancho: Optional[float]
    alto: Optional[float]
    peso: Optional[float]
    peso_volumetrico: Optional[float]

@router.put("/caja/{caja_id}")
def editar_caja(caja_id: int, data: CajaUpdate, db: Session = Depends(get_db)):
    caja = db.query(Caja).filter(Caja.id == caja_id).first()
    if not caja:
        raise HTTPException(status_code=404, detail="Caja no encontrada")

    if data.paqueteria:
        caja.paqueteria = PaqueteriaEnum(data.paqueteria)
    if data.tipo_embalaje:
        caja.tipo_embalaje = TipoEmbalajeEnum(data.tipo_embalaje)

    for field, value in data.dict(exclude_unset=True).items():
        if field not in ["paqueteria", "tipo_embalaje"]:
            setattr(caja, field, value)

    caja.fecha_hora = datetime.now()
    db.commit()
    db.refresh(caja)
    return {"mensaje": "Caja actualizada correctamente"}

# ------------------------------------------------------------------
# ✏️ PUT: Editar Tarima
# ------------------------------------------------------------------
class TarimaUpdate(BaseModel):
    numero_factura: Optional[str]
    paqueteria: Optional[str]
    cantidad_piezas: Optional[int]
    clave_producto: Optional[str]
    tipo_embalaje: Optional[str]
    largo: Optional[float]
    ancho: Optional[float]
    alto: Optional[float]
    peso: Optional[float]
    peso_volumetrico: Optional[float]

@router.put("/tarima/{tarima_id}")
def editar_tarima(tarima_id: int, data: TarimaUpdate, db: Session = Depends(get_db)):
    tarima = db.query(Tarima).filter(Tarima.id == tarima_id).first()
    if not tarima:
        raise HTTPException(status_code=404, detail="Tarima no encontrada")

    if data.paqueteria:
        tarima.paqueteria = PaqueteriaEnum(data.paqueteria)
    if data.tipo_embalaje:
        tarima.tipo_embalaje = TipoEmbalajeEnum(data.tipo_embalaje)

    for field, value in data.dict(exclude_unset=True).items():
        if field not in ["paqueteria", "tipo_embalaje"]:
            setattr(tarima, field, value)

    tarima.fecha_hora = datetime.now()
    db.commit()
    db.refresh(tarima)
    return {"mensaje": "Tarima actualizada correctamente"}
