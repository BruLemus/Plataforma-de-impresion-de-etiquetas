# app/db/models/user_practicante.py
import enum
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from app.db.database import Base
from app.db.models.enums import mesaTrabajoEnum

# 🔹 Contexto para hashear contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔹 Modelo UserPracticante
class UserPracticanteMX(Base):
    __tablename__ = "user_practicantes_mx"

    # 🔹 Campos principales
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    contrasena = Column(String(100), nullable=False)  # almacenar hash
    mesa_trabajo = Column(Enum(mesaTrabajoEnum, native_enum=False), nullable=True)

    # 🔹 Relaciones
    cajas = relationship("Caja", back_populates="practicante_mx")
    tarimas = relationship("Tarima", back_populates="practicante_mx")

    # 🔹 Métodos de contraseña
    def set_password(self, password: str):
        """Hashea la contraseña y la guarda en el campo 'contrasena'"""
        self.contrasena = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Verifica la contraseña ingresada contra el hash almacenado"""
        return pwd_context.verify(password, self.contrasena)
