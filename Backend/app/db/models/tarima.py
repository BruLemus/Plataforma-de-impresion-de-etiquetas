import enum
from sqlalchemy import Column, Integer, String, Float, Enum, DateTime
from sqlalchemy.sql import func
from app.db.database import Base  
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.models.enums import PaqueteriaEnum
from datetime import datetime


class TipoEmbalajeEnum(int, enum.Enum):
    TIPO1 = 1
    TIPO2 = 2
    TIPO3 = 3

class Tarima(Base):
    __tablename__ = "tarimas"

    id = Column(Integer, primary_key=True, index=True)
    numero_facturas = Column(String(100), nullable=False)
    numero_tarimas = Column(Integer, nullable=False)
    tipo_embalaje = Column(Enum(TipoEmbalajeEnum), nullable=False)
    paqueteria = Column(Enum(PaqueteriaEnum), nullable=False)
    clave_producto = Column(String(100), nullable=False)
    cantidad_piezas = Column(Integer, nullable=True)
    ancho = Column(Float, default=0)
    largo = Column(Float, default=0)
    alto = Column(Float, default=0)
    peso = Column(Float, default=0)
    peso_volumetrico = Column(Float, default=0)
    fecha_hora = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    practicante_id = Column(Integer, ForeignKey("user_practicantes.user_id"), nullable=True)
    coordinador_id = Column(Integer, ForeignKey("user_coordinadores.id"), nullable=True)
    nombre_creador = Column(String(100), nullable=True)

    practicante = relationship("UserPracticante", back_populates="tarimas")
    coordinador = relationship("UserCoordinador", back_populates="tarimas")