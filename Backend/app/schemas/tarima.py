from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.db.models.tarima import PaqueteriaEnum, TipoEmbalajeEnum


class TarimaBase(BaseModel):
    nombre_user_practicante: Optional[str] = None
    nombre_user_coordinador: Optional[str] = None
    n_facturas: str
    n_tarimas: int
    paqueteria: PaqueteriaEnum
    t_embalaje: TipoEmbalajeEnum
    clave_producto: str
    cantidad_piezas: Optional[int] = None
    ancho: float
    largo: float
    alto: float
    peso: float
    peso_volumetrico: Optional[float] = None


class TarimaCreate(TarimaBase):
    practicante_id: Optional[int] = None
    coordinador_id: Optional[int] = None


class TarimaRead(TarimaBase):
    id: int
    fecha_hora: datetime
    practicante_id: Optional[int] = None
    coordinador_id: Optional[int] = None

    class Config:
        from_attributes = True
