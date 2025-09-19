from pydantic import BaseModel



class UserPracticanteBase(BaseModel):
    nombre: str
    mesa_trabajo: str | None = None
    entrada: int | None = None
    salida: int | None = None

class UserPracticanteCreate(UserPracticanteBase):
    pass

class UserPracticanteUpdate(UserPracticanteBase):
    pass

class UserPracticanteInDB(UserPracticanteBase):
    user_id: int

    class Config:
        orm_mode = True
        
class UserPracticanteResponse(BaseModel):
    user_id: int
    nombre: str
    mesa_trabajo: str | None = None
    entrada: int | None = None
    salida: int | None = None

    class Config:
        orm_mode = True