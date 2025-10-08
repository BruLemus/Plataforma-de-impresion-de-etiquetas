from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.user_practicante import UserPracticanteCreate, UserPracticanteUpdate, UserPracticanteResponse
from app.services import user_practicante
from app.core.security import create_access_token
from datetime import timedelta

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
def login_user_practicante(nombre: str, contrasena: str, db: Session = Depends(get_db)):
    db_user = db.query(user_practicante.UserPracticante).filter(user_practicante.UserPracticante.nombre == nombre).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    if not db_user.verify_password(contrasena):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": db_user.nombre, "user_id": db_user.user_id},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer", "user_id": db_user.user_id, "nombre": db_user.nombre}
