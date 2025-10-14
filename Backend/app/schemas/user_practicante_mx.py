from pydantic import BaseModel
from typing import Optional

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
    user_id: int
    token: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
