from datetime import datetime
from pydantic import BaseModel
from app.db.models.enums import UserRoleEnum, mesaTrabajoEnum

class UserRolBase(BaseModel):
    nombre: str
    UserRol: UserRoleEnum
    contrasena: str
    mesa_trabajo: mesaTrabajoEnum
    entrada: datetime
    salida: datetime | None = None
    
class UserRolCreate(UserRolBase):
    pass

class UserRolRead(UserRolBase):
    user_rol_id: int

    class Config:
        from_attributes = True
        