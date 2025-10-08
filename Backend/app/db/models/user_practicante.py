import enum
from sqlalchemy import Column, Integer, String, Enum
from app.db.database import Base
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

# 🔹 Contexto para hashear contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔹 Modelo User_practicante
class UserPracticante(Base):
    __tablename__ = "user_practicantes"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    contrasena = Column(String(100), nullable=False)  # almacenar hash
    mesa_trabajo = Column(String(100), nullable=True)

    # 🔹 Relación correcta
    cajas = relationship("Caja", back_populates="practicante")
    tarimas = relationship("Tarima", back_populates="practicante")

    # 🔹 Métodos de contraseña
    def set_password(self, password: str):
        self.contrasena = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.contrasena)
