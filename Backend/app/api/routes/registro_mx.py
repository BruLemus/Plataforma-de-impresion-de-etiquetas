# app/routers/registros_mx.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.db.database import get_db
from app.db.models.caja_mx import Caja_mx
from app.db.models.tarima_mx import Tarima_mx
from app.db.models.enums import PaqueteriaEnum, TipoEmbalajeEnum
from pydantic import BaseModel

router = APIRouter()


# ------------------------------------------------------------------
# ✏️ Modelo para actualización
# ------------------------------------------------------------------
class RegistroUpdate(BaseModel):
    numero_factura: Optional[str] = None
    paqueteria: Optional[str] = None
    cantidad_piezas: Optional[int] = None
    clave_producto: Optional[str] = None
    tipo_embalaje: Optional[int] = None
    largo: Optional[float] = None
    ancho: Optional[float] = None
    alto: Optional[float] = None
    peso: Optional[float] = None
    peso_volumetrico: Optional[float] = None
    numero_tarimas: Optional[int] = None  # Solo para Tarimas


# ------------------------------------------------------------------
# ✅ GET: Obtener todos los registros (Cajas y Tarimas)
# ------------------------------------------------------------------
@router.get("/")
def obtener_registros(db: Session = Depends(get_db)):
    registros = []

    # 🔹 Cajas
    cajas = db.query(Caja_mx).all()
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

    # 🔹 Tarimas
    tarimas = db.query(Tarima_mx).all()
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

    registros.sort(key=lambda x: x["fecha_creacion"], reverse=True)
    return registros


# ------------------------------------------------------------------
# 🗑️ DELETE: Caja o Tarima
# ------------------------------------------------------------------
@router.delete("/caja/{caja_id}")
def eliminar_caja(caja_id: int, db: Session = Depends(get_db)):
    caja = db.query(Caja_mx).filter(Caja_mx.id == caja_id).first()
    if not caja:
        raise HTTPException(status_code=404, detail="Caja no encontrada")
    db.delete(caja)
    db.commit()
    return {"mensaje": "Caja eliminada correctamente"}


@router.delete("/tarima/{tarima_id}")
def eliminar_tarima(tarima_id: int, db: Session = Depends(get_db)):
    tarima = db.query(Tarima_mx).filter(Tarima_mx.id == tarima_id).first()
    if not tarima:
        raise HTTPException(status_code=404, detail="Tarima no encontrada")
    db.delete(tarima)
    db.commit()
    return {"mensaje": "Tarima eliminada correctamente"}


# ------------------------------------------------------------------
# ✏️ PUT: Unificado - Editar Caja o Tarima según tipo
# ------------------------------------------------------------------
@router.put("/{tipo}/{registro_id}")
def editar_registro(tipo: str, registro_id: int, data: RegistroUpdate, db: Session = Depends(get_db)):
    tipo = tipo.lower()
    if tipo not in ["caja", "tarima"]:
        raise HTTPException(status_code=400, detail="Tipo inválido, debe ser 'caja' o 'tarima'")

    modelo = Caja_mx if tipo == "caja" else Tarima_mx
    registro = db.query(modelo).filter(modelo.id == registro_id).first()
    if not registro:
        raise HTTPException(status_code=404, detail=f"{tipo.capitalize()} no encontrada")

    # 🔹 Validación y asignación de enums
    if data.paqueteria:
        try:
            registro.paqueteria = PaqueteriaEnum(data.paqueteria)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Paquetería inválida: {data.paqueteria}")

    if data.tipo_embalaje is not None:
        campo_enum = "t_embalaje" if tipo == "caja" else "tipo_embalaje"
        try:
            setattr(registro, campo_enum, TipoEmbalajeEnum(data.tipo_embalaje))
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Tipo de embalaje inválido: {data.tipo_embalaje}")

    # 🔹 Campos comunes
    for field, value in data.dict(exclude_unset=True).items():
        if field not in ["paqueteria", "tipo_embalaje"]:
            if hasattr(registro, field):
                setattr(registro, field, value)

    registro.fecha_hora = datetime.now()
    db.commit()
    db.refresh(registro)

    return {"mensaje": f"{tipo.capitalize()} actualizada correctamente", "registro": registro}
