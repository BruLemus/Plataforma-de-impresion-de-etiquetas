import enum 
from sqlalchemy import Column, Integer, String, Enum
from app.db.database import Base  # tu Base de SQLAlchemy
# 🔹 Modelo User_practicante

class UserPracticante(Base):
    __tablename__ = "user_practicantes"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    mesa_trabajo = Column(String(100), nullable=True)  # Nuevo campo opcional
    entrada = Column(Integer, nullable=True)  # Nuevo campo opcional
    salida = Column(Integer, nullable=True)  # Nuevo campo opcional