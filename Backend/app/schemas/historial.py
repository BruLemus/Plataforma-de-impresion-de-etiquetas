from pydantic import BaseModel
from datetime import datetime

class HistorialSchema(BaseModel):
    usuario: str
    tipo_usuario: str
    numero_factura: str
    cantidad_piezas: int | None
    tipo_embalaje: str | None
    tipo_pedido: str
    paqueteria: str | None
    clave_producto: str | None
    fecha_creacion: datetime | None

    class Config:
        orm_mode = True
