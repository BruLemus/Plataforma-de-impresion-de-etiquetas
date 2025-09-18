from datetime import datetime
from pydantic import BaseModel
from app.db.models.enums import PaqueteriaEnum, TipoEmbalajeEnum

class CajaBase(BaseModel):
    paqueteria: PaqueteriaEnum
    numero_factura: str
    numero_cajas: int
    tipo_embalaje: TipoEmbalajeEnum
    ancho: float
    largo: float
    alto: float
    peso: float
    cantidad_piezas: int | None = None
    clave_producto: str

class CajaCreate(CajaBase):
    pass

class CajaRead(CajaBase):
    id: int
    fecha_creacion: datetime  # <-- nuevo

    class Config:
        from_attributes = True


