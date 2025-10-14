
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from app.db.database import Base
from app.db.models.enums import mesaTrabajoEnum

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserPracticanteMX(Base):
    __tablename__ = "user_practicantes_mx"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False) 
    contrasena = Column(String(100), nullable=False)
    mesa_trabajo = Column(Enum(mesaTrabajoEnum, native_enum=False), nullable=True)

    # Relaciones
    cajas_mx = relationship("CajaMX", back_populates="practicante")
    tarimas_mx = relationship("TarimaMX", back_populates="practicante")

    # Métodos de contraseña
    def set_password(self, password: str):
        self.contrasena = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.contrasena)
