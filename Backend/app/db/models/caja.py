from sqlalchemy import Column, Integer, String, Float, Enum, DateTime
from sqlalchemy.sql import func
from app.db.database import Base
from app.db.models.enums import PaqueteriaEnum, TipoEmbalajeEnum

class Caja(Base):
    __tablename__ = "cajas"

    id = Column(Integer, primary_key=True, index=True)
    paqueteria = Column(Enum(PaqueteriaEnum), nullable=False)
    numero_factura = Column(String(50), nullable=False)
    numero_cajas = Column(Integer, nullable=False)
    tipo_embalaje = Column(Enum(TipoEmbalajeEnum), nullable=False)
    ancho = Column(Float, nullable=False)
    largo = Column(Float, nullable=False)
    alto = Column(Float, nullable=False)
    peso = Column(Float, nullable=False)
    cantidad_piezas = Column(Integer, nullable=True)
    clave_producto = Column(String(50), nullable=False)
    
    # Fecha y hora de creación automática
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
