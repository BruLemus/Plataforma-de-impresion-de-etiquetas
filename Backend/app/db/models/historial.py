from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base

class Historial(Base):
    __tablename__ = "historial"  # Puede ser solo para mapeo o una tabla física

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String(100), nullable=False)
    tipo_usuario = Column(String(50), nullable=False)  # Coordinador o Practicante
    numero_factura = Column(String(50), nullable=False)
    cantidad_piezas = Column(Integer, nullable=True)
    tipo_embalaje = Column(String(50), nullable=True)
    tipo_pedido = Column(String(50), nullable=True)  # Caja o Tarima
    paqueteria = Column(String(50), nullable=True)
    clave_producto = Column(String(100), nullable=True)
    fecha_creacion = Column(DateTime, nullable=True)
