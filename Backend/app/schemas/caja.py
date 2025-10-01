from datetime import datetime
from pydantic import BaseModel
from app.db.models.enums import PaqueteriaEnum, TipoEmbalajeEnum
from typing import Optional

class CajaBase(BaseModel):
    paqueteria: PaqueteriaEnum
    numero_factura: str
    numero_cajas: int
    tipo_embalaje: TipoEmbalajeEnum
    ancho: float
    largo: float
    alto: float
    peso: float
    cantidad_piezas: Optional[int] = None
    clave_producto: str

class CajaCreate(CajaBase):
    pass

class CajaRead(CajaBase):
    id: int
    fecha_creacion: datetime
    coordinador_nombre: Optional[str] = None  
    practicante_nombre: Optional[str] = None  

    class Config:
        from_attributes = True
