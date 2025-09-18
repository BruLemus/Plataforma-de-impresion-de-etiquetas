from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Enum
from sqlalchemy.sql import func
from app.db.database import Base  # tu Base de SQLAlchemy
from app.db.models.enums import UserRoleEnum, mesaTrabajoEnum  # Asegúrate de tener este enum definido



class UserRol(Base):
    __tablename__ = "user_rol"

    user_rol_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    UserRol = Column(Enum(UserRoleEnum), nullable=False)
    contrasena = Column(String(255), nullable=False)
    mesa_trabajo = Column(Enum(mesaTrabajoEnum), nullable=False)
    entrada = Column(DateTime(timezone=True), server_default=func.now())
    salida = Column(DateTime(timezone=True), nullable=True)