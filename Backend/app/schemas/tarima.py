from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.db.models.tarima import PaqueteriaEnum, TipoEmbalajeEnum

class TarimaBase(BaseModel):
    numero_facturas: str
    numero_tarimas: int
    paqueteria: PaqueteriaEnum
    tipo_embalaje: TipoEmbalajeEnum
    clave_producto: str
    cantidad_piezas: Optional[int] = 0
    ancho: Optional[float] = 0
    largo: Optional[float] = 0
    alto: Optional[float] = 0
    peso: Optional[float] = 0
    peso_volumetrico: Optional[float] = 0
    practicante_id: Optional[int] = None
    coordinador_id: Optional[int] = None

class TarimaCreate(TarimaBase):
    pass

class TarimaRead(TarimaBase):
    id: int
    fecha_hora: datetime
    nombre_creador: Optional[str] = None

    class Config:
        fromm_orm = True
