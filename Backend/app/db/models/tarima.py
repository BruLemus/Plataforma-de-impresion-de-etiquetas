import enum
from sqlalchemy import Column, Integer, String, Float, Enum, DateTime
from sqlalchemy.sql import func
from app.db.database import Base  
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

# 🔹 Enums
class PaqueteriaEnum(str, enum.Enum):
    PAQUETEXPRESS = "Paquetexpress"
    ESTAFETA = "Estafeta"
    DHL = "DHL"
    FEDEX = "FedEx"
    UPS = "UPS"
    MERCADO_LIBRE = "MercadoLibre"

class TipoEmbalajeEnum(int, enum.Enum):
    TIPO1 = 1
    TIPO2 = 2
    TIPO3 = 3

# 🔹 Modelo Tarima
class Tarima(Base):
    __tablename__ = "tarimas"

    tarima_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    paqueteria = Column(Enum(PaqueteriaEnum), nullable=False)
    numero_factura = Column(String(50), nullable=False)
    numero_tarimas = Column(Integer, nullable=False)
    tipo_embalaje = Column(Enum(TipoEmbalajeEnum), nullable=False)
    ancho = Column(Float, nullable=False)
    largo = Column(Float, nullable=False)
    alto = Column(Float, nullable=False)
    cantidad_piezas = Column(Integer, nullable=True)
    clave_producto = Column(String(100), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    coordinador_id = Column(Integer, ForeignKey("user_coordinadores.id"), nullable=True)
    practicante_id = Column(Integer, ForeignKey("user_practicantes.user_id"), nullable=True)

    coordinador = relationship("UserCoordinador", back_populates="tarimas")
    practicante = relationship("UserPracticante", back_populates="tarimas")
