from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.user_practicante import UserPracticanteCreate, UserPracticanteUpdate, UserPracticanteResponse
from app.services import user_practicante
from app.core.security import create_access_token
from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.user_practicante import UserPracticante
from app.core.security import pwd_context, create_access_token

router = APIRouter()

# 🔹 Crear usuario
@router.post("/", response_model=UserPracticanteResponse)
def create_user_practicante_endpoint(payload: UserPracticanteCreate, db: Session = Depends(get_db)):
    return user_practicante.create_user_practicante(db, payload)

# 🔹 Listar todos
@router.get("/", response_model=List[UserPracticanteResponse])
def list_user_practicantes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_practicante.get_user_practicantes(db, skip=skip, limit=limit)

# 🔹 Obtener uno por ID
@router.get("/{user_id}", response_model=UserPracticanteResponse)
def get_user_practicante(user_id: int, db: Session = Depends(get_db)):
    db_user = user_practicante.get_user_practicante_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario practicante no encontrado")
    return db_user

# 🔹 Actualizar
@router.put("/{user_id}", response_model=UserPracticanteResponse)
def update_user_practicante_endpoint(user_id: int, payload: UserPracticanteUpdate, db: Session = Depends(get_db)):
    db_user = user_practicante.update_user_practicante(db, user_id, payload)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario practicante no encontrado")
    return db_user

# 🔹 Eliminar
@router.delete("/{user_id}")
def delete_user_practicante_endpoint(user_id: int, db: Session = Depends(get_db)):
    deleted = user_practicante.delete_user_practicante(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuario practicante no encontrado")
    return {"detail": "Usuario practicante eliminado correctamente"}

# 🔹 LOGIN practicante

@router.post("/login")
def login_practicante(
    nombre: str = Form(...),
    contrasena: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(UserPracticante).filter(UserPracticante.nombre == nombre).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not pwd_context.verify(contrasena, user.contrasena):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    token = create_access_token({"sub": user.nombre})
    return {"token": token, "nombre": user.nombre, "user_id": user.user_id}
