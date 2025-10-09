# app/schemas/tarima_schemas.py
from pydantic import BaseModel
from typing import Optional
from app.db.models.tarima import TipoEmbalajeEnum
from app.db.models.enums import PaqueteriaEnum
from datetime import datetime

class TarimaCreate(BaseModel):
    numero_facturas: str
    numero_tarimas: int
    tipo_embalaje: TipoEmbalajeEnum
    paqueteria: PaqueteriaEnum
    clave_producto: str
    cantidad_piezas: Optional[int] = 0
    ancho: Optional[float] = 0
    largo: Optional[float] = 0
    alto: Optional[float] = 0
    peso: Optional[float] = 0
    peso_volumetrico: Optional[float] = 0

class TarimaUpdate(BaseModel):
    numero_facturas: Optional[str]
    numero_tarimas: Optional[int]
    tipo_embalaje: Optional[TipoEmbalajeEnum]
    paqueteria: Optional[PaqueteriaEnum]
    clave_producto: Optional[str]
    cantidad_piezas: Optional[int]
    ancho: Optional[float]
    largo: Optional[float]
    alto: Optional[float]
    peso: Optional[float]
    peso_volumetrico: Optional[float]

class TarimaResponse(BaseModel):
    id: int
    numero_facturas: str
    numero_tarimas: int
    tipo_embalaje: TipoEmbalajeEnum
    paqueteria: PaqueteriaEnum
    clave_producto: str
    cantidad_piezas: Optional[int]
    ancho: Optional[float]
    largo: Optional[float]
    alto: Optional[float]
    peso: Optional[float]
    peso_volumetrico: Optional[float]
    coordinador_nombre: Optional[str]
    practicante_nombre: Optional[str]
    coordinador_id: Optional[int]
    practicante_id: Optional[int]
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]

    class Config:
        from_orm = True