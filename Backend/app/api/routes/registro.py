from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.db.database import get_db
from app.db.models.caja import Caja
from app.db.models.tarima import Tarima, PaqueteriaEnum, TipoEmbalajeEnum
from pydantic import BaseModel

router = APIRouter(prefix="/registros", tags=["Registros"])

# -------------------------
# ✅ GET: Obtener todos los registros (Cajas + Tarimas)
# -------------------------
@router.get("/")
def obtener_registros(db: Session = Depends(get_db)):
    registros = []

    # 🔹 Cajas
    cajas = db.query(Caja).all()
    for c in cajas:
        usuario = c.nombre_user_coordinador or c.nombre_user_practicante or "Desconocido"
        registros.append({
            "id": c.id,
            "nombre_usuario": usuario,
            "factura": c.n_facturas,
            "cantidad": c.n_cajas,
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
    tarimas = db.query(Tarima).all()
    for t in tarimas:
        usuario = t.coordinador_nombre or t.practicante_nombre or "Desconocido"
        registros.append({
            "id": t.id,
            "nombre_usuario": usuario,
            "factura": t.numero_facturas,
            "cantidad": t.numero_tarimas,
            "tipo_embalaje": t.tipo_embalaje.value if t.tipo_embalaje else None,
            "paqueteria": t.paqueteria.value if t.paqueteria else None,
            "clave_producto": t.clave_producto,
            "tipo_pedido": "Tarima",
            "fecha_creacion": t.fecha_creacion,
            "largo": t.largo,
            "ancho": t.ancho,
            "alto": t.alto,
            "peso": t.peso,
            "peso_volumetrico": t.peso_volumetrico
        })

    # Ordenar por fecha más reciente
    registros.sort(key=lambda x: x["fecha_creacion"], reverse=True)
    return registros


# -------------------------
# 🗑️ DELETE: Eliminar Caja o Tarima
# -------------------------
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


# -------------------------
# ✏️ PUT: Editar Tarima
# -------------------------
class TarimaUpdate(BaseModel):
    numero_facturas: Optional[str]
    paqueteria: Optional[str]
    tipo_embalaje: Optional[int]
    numero_tarimas: Optional[int]
    clave_producto: Optional[str]
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
    if data.tipo_embalaje is not None:
        tarima.tipo_embalaje = TipoEmbalajeEnum(data.tipo_embalaje)

    for field, value in data.dict(exclude_unset=True).items():
        if field not in ["paqueteria", "tipo_embalaje"]:
            setattr(tarima, field, value)

    tarima.fecha_actualizacion = datetime.now()
    db.commit()
    db.refresh(tarima)
    return {"mensaje": "Tarima actualizada correctamente"}


# -------------------------
# ✏️ POST: Crear Tarima
# -------------------------
class TarimaCreate(BaseModel):
    numero_facturas: str
    numero_tarimas: int
    paqueteria: str
    tipo_embalaje: int
    clave_producto: str
    numero_piezas: int
    largo: float = 0
    ancho: float = 0
    alto: float = 0
    peso: float = 0
    peso_volumetrico: float = 0
    practicante_id: Optional[int] = None
    coordinador_id: Optional[int] = None
    nombre_creador: str

@router.post("/tarima/")
def crear_tarima(payload: TarimaCreate, db: Session = Depends(get_db)):
    tarima = Tarima(
        numero_facturas=payload.numero_facturas,
        numero_tarimas=payload.numero_tarimas,
        paqueteria=PaqueteriaEnum(payload.paqueteria),
        tipo_embalaje=TipoEmbalajeEnum(payload.tipo_embalaje),
        clave_producto=payload.clave_producto,
        cantidad_piezas=payload.numero_piezas,
        largo=payload.largo,
        ancho=payload.ancho,
        alto=payload.alto,
        peso=payload.peso,
        peso_volumetrico=payload.peso_volumetrico,
        practicante_id=payload.practicante_id,
        coordinador_id=payload.coordinador_id,
        practicante_nombre=payload.nombre_creador if payload.practicante_id else None,
        coordinador_nombre=payload.nombre_creador if payload.coordinador_id else None,
        fecha_creacion=datetime.now(),
    )
    db.add(tarima)
    db.commit()
    db.refresh(tarima)
    return tarima
