from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
from app.db.database import get_db
from app.db.models.caja import Caja
from app.db.models.tarima import Tarima
from app.db.models.enums import PaqueteriaEnum, TipoEmbalajeEnum
from app.db.models.user_coordinador import UserCoordinador
from app.db.models.user_practicante import UserPracticante
from pydantic import BaseModel

router = APIRouter(prefix="/registros", tags=["Registros"])

# ------------------------------------------------------------------
# ✅ GET: Obtener todos los registros (Cajas y Tarimas)
# ------------------------------------------------------------------

@router.get("/")
def obtener_registros(db: Session = Depends(get_db)):
    result = []

    # ----------------------
    # Cajas
    # ----------------------
    cajas = db.query(Caja).all()
    for c in cajas:
        usuario = c.nombre_user_coordinador or c.nombre_user_practicante or "Desconocido"

        result.append({
            "id": c.id,
            "nombre_usuario": usuario,
            "factura": c.n_facturas,
            "cantidad": c.cantidad_piezas,
            "tipo_embalaje": c.t_embalaje.value if c.t_embalaje else None,
            "paqueteria": c.paqueteria.value if c.paqueteria else None,
            "clave_producto": c.clave_producto,
            "tipo_pedido": "Caja",
            "fecha_creacion": c.fecha_hora,
            "acciones": {"editar": f"/caja/{c.id}", "eliminar": f"/caja/{c.id}"}
        })

    # ----------------------
    # Tarimas
    # ----------------------
    tarimas = db.query(Tarima).all()
    for t in tarimas:
        usuario = t.coordinador_nombre or t.practicante_nombre or "Desconocido"

        result.append({
            "id": t.tarima_id,
            "nombre_usuario": usuario,
            "factura": t.numero_factura,
            "cantidad": t.cantidad_piezas,
            "tipo_embalaje": t.tipo_embalaje.value if t.tipo_embalaje else None,
            "paqueteria": t.paqueteria.value if t.paqueteria else None,
            "clave_producto": t.clave_producto,
            "tipo_pedido": "Tarima",
            "fecha_creacion": t.fecha_creacion,
            "acciones": {"editar": f"/tarima/{t.tarima_id}", "eliminar": f"/tarima/{t.tarima_id}"}
        })

    # Ordenar por fecha
    result.sort(key=lambda x: x["fecha_creacion"])
    return result

    registros = []

    # 🔹 Obtener cajas
    cajas = db.query(Caja).all()
    for c in cajas:
        usuario = "Desconocido"
        if c.coordinador:
            usuario = c.coordinador.nombre
        elif c.practicante:
            usuario = c.practicante.nombre

        registros.append({
            "id": c.id,
            "nombre_usuario": usuario,
            "factura": c.numero_factura,
            "cantidad": c.cantidad_piezas,
            "tipo_embalaje": c.tipo_embalaje.value if c.tipo_embalaje else None,
            "paqueteria": c.paqueteria.value if c.paqueteria else None,
            "clave_producto": c.clave_producto,
            "tipo_pedido": "Caja",
            "fecha_creacion": c.fecha_creacion,
        })

    # 🔹 Obtener tarimas
    tarimas = db.query(Tarima).all()
    for t in tarimas:
        usuario = "Desconocido"
        if t.coordinador:
            usuario = t.coordinador.nombre
        elif t.practicante:
            usuario = t.practicante.nombre

        registros.append({
            "id": t.tarima_id,
            "nombre_usuario": usuario,
            "factura": t.numero_factura,
            "cantidad": t.cantidad_piezas,
            "tipo_embalaje": t.tipo_embalaje.value if t.tipo_embalaje else None,
            "paqueteria": t.paqueteria.value if t.paqueteria else None,
            "clave_producto": t.clave_producto,
            "tipo_pedido": "Tarima",
            "fecha_creacion": t.fecha_creacion,
        })

    # 🔹 Ordenar por fecha más reciente
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
    tarima = db.query(Tarima).filter(Tarima.tarima_id == tarima_id).first()
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

@router.put("/caja/{caja_id}")
def editar_caja(caja_id: int, data: CajaUpdate, db: Session = Depends(get_db)):
    caja = db.query(Caja).filter(Caja.id == caja_id).first()
    if not caja:
        raise HTTPException(status_code=404, detail="Caja no encontrada")

    # Validar enums
    if data.paqueteria:
        caja.paqueteria = PaqueteriaEnum(data.paqueteria)
    if data.tipo_embalaje:
        caja.tipo_embalaje = TipoEmbalajeEnum(data.tipo_embalaje)

    # Actualizar otros campos
    for field, value in data.dict(exclude_unset=True).items():
        if field not in ["paqueteria", "tipo_embalaje"]:
            setattr(caja, field, value)

    caja.fecha_actualizacion = datetime.now()
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

@router.put("/tarima/{tarima_id}")
def editar_tarima(tarima_id: int, data: TarimaUpdate, db: Session = Depends(get_db)):
    tarima = db.query(Tarima).filter(Tarima.tarima_id == tarima_id).first()
    if not tarima:
        raise HTTPException(status_code=404, detail="Tarima no encontrada")

    if data.paqueteria:
        tarima.paqueteria = PaqueteriaEnum(data.paqueteria)
    if data.tipo_embalaje:
        tarima.tipo_embalaje = TipoEmbalajeEnum(data.tipo_embalaje)

    for field, value in data.dict(exclude_unset=True).items():
        if field not in ["paqueteria", "tipo_embalaje"]:
            setattr(tarima, field, value)

    tarima.fecha_actualizacion = datetime.now()
    db.commit()
    db.refresh(tarima)
    return {"mensaje": "Tarima actualizada correctamente"}
