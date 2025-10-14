from pydantic import BaseModel
from typing import Optional
from app.db.models.enums import mesaTrabajoEnum

class UserPracticanteMXBase(BaseModel):
    nombre: str
    mesa_trabajo: Optional[str] = None

class UserPracticanteMXCreate(UserPracticanteMXBase):
    contrasena: str

class UserPracticanteMXLogin(BaseModel):
    nombre: str
    contrasena: str

class UserPracticanteMXUpdate(BaseModel):
    nombre: Optional[str] = None
    contrasena: Optional[str] = None
    mesa_trabajo: Optional[str] = None

class UserPracticanteMXResponse(UserPracticanteMXBase):
    id: int
    nombre: str
    mesa_trabajo: mesaTrabajoEnum

    model_config = {
        "from_attributes": True
    }
