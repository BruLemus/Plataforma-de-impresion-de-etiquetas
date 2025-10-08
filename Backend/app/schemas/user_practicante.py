from pydantic import BaseModel, Field

# 🔹 Base común
class UserPracticanteBase(BaseModel):
    nombre: str
    mesa_trabajo: int | None = None

# 🔹 Esquema para crear usuario (incluye contraseña)
class UserPracticanteCreate(UserPracticanteBase):
    contrasena: str = Field(..., min_length=6)  # obligatoria al crear usuario

# 🔹 Esquema para actualizar usuario (opcional)
class UserPracticanteUpdate(UserPracticanteBase):
    contrasena: str | None = Field(None, min_length=6)  # opcional al actualizar

# 🔹 Esquema interno que incluye ID y contraseña (para la DB)
class UserPracticanteInDB(UserPracticanteBase):
    user_id: int
    contrasena: str  # hash de la contraseña

    class Config:
        from_attributes = True

# 🔹 Esquema de respuesta al cliente (sin contraseña)
class UserPracticanteResponse(BaseModel):
    user_id: int
    nombre: str
    mesa_trabajo: str | None = None

    class Config:
        from_attributes = True
