from pydantic import BaseModel  
from typing import Optional
from datetime import datetime
from app.db.models.tarima import PaqueteriaEnum, TipoEmbalajeEnum

class TarimaCreate(BaseModel):
    paqueteria: PaqueteriaEnum
    numero_factura: str
    numero_tarimas: int
    tipo_embalaje: TipoEmbalajeEnum
    ancho: float
    largo: float
    alto: float
    cantidad_piezas: Optional[int] = None
    clave_producto: str

class TarimaRead(TarimaCreate):
    tarima_id: int
    fecha_creacion: datetime

    class Config:
       from_attributes = True 
