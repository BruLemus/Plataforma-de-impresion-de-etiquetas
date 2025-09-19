from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.user_coordinador import UserCoordinador
from app.schemas.user_coordinador import UserCoordinadorCreate, UserCoordinadorResponse
from typing import List
from passlib.context import CryptContext
from app.db.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_CODE = "UPPER" 


# Obtener todos los coordinadores
@router.get("/", response_model=List[UserCoordinadorResponse])
def get_all_coordinadores(db: Session = Depends(get_db)):
    return db.query(UserCoordinador).all()

# Crear coordinador
@router.post("/", response_model=UserCoordinadorResponse)
def create_coordinador(payload: UserCoordinadorCreate, db: Session = Depends(get_db)):
    if payload.codigo_secreto != SECRET_CODE:
        raise HTTPException(status_code=403, detail="Código secreto incorrecto")
    
    hashed_password = pwd_context.hash(payload.contrasena)
    user = UserCoordinador(
        nombre=payload.nombre,
        contrasena=hashed_password,
        codigo_secreto=payload.codigo_secreto
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Eliminar coordinador por ID
@router.delete("/{coordinador_id}")
def delete_coordinador(coordinador_id: int, db: Session = Depends(get_db)):
    user = db.query(UserCoordinador).filter(UserCoordinador.id == coordinador_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Coordinador no encontrado")
    db.delete(user)
    db.commit()
    return {"detail": "Coordinador eliminado"}
