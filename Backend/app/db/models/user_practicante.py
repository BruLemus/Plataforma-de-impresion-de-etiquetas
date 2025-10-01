
import enum 
from sqlalchemy import Column, Integer, String, Enum 
from app.db.database import Base  # tu Base de SQLAlchemy
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship


# 🔹 Modelo User_practicante
class UserPracticante(Base):
    __tablename__ = "user_practicantes"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    mesa_trabajo = Column(String(100), nullable=True)
    entrada = Column(BIGINT, nullable=True)

    # 🔹 Relación correcta
    cajas = relationship("Caja", back_populates="practicante")
    tarimas = relationship("Tarima", back_populates="practicante")
