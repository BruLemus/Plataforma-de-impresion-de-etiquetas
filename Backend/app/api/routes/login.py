from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.models.user_coordinador import UserCoordinador
from app.db.models.user_practicante import UserPracticante
from app.schemas.user_coordinador import UserCoordinadorResponse
from app.schemas.user_practicante import UserPracticanteResponse
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

router = APIRouter()

# ---------------------------
# Seguridad y hashing
# ---------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "SUPER_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200  #DURACION DEL TOKEN DE 12 HORAS

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ---------------------------
# Login dinámico según ciudad y tipo
# ---------------------------
@router.post("/{ciudad}/{tipo}/")
def login(ciudad: str, tipo: str, nombre: str = Form(...), contrasena: str = Form(...), db: Session = Depends(get_db)):
    tipo = tipo.lower()

    if tipo == "coordinador":
        user = db.query(UserCoordinador).filter(UserCoordinador.nombre == nombre).first()
        if not user or not verify_password(contrasena, user.contrasena):
            raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
        token = create_access_token({"user_id": user.id})
        return {"nombre": user.nombre, "token": token, "ciudad": ciudad, "tipo": tipo}

    elif tipo == "practicante":
        user = db.query(UserPracticante).filter(UserPracticante.nombre == nombre).first()
        if not user or not verify_password(contrasena, user.contrasena):
            raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
        return {"nombre": user.nombre, "ciudad": ciudad, "tipo": tipo}

    else:
        raise HTTPException(status_code=400, detail="Tipo de usuario inválido")

# ---------------------------
# Endpoints de ejemplo protegidos
# ---------------------------
def get_current_user(role: str, token: str = None, db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Token requerido")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    if role == "coordinador":
        user = db.query(UserCoordinador).filter(UserCoordinador.id == user_id).first()
    elif role == "practicante":
        user = db.query(UserPracticante).filter(UserPracticante.user_id == user_id).first()
    else:
        raise HTTPException(status_code=400, detail="Rol inválido")

    if not user:
        raise HTTPException(status_code=401, detail=f"{role.capitalize()} no encontrado")

    return user

@router.get("/{ciudad}/{tipo}/dashboard")
def dashboard(ciudad: str, tipo: str, token: str = None, db: Session = Depends(get_db)):
    user = get_current_user(tipo, token, db)
    return {"msg": f"Hola {user.nombre}, bienvenido a tu dashboard en {ciudad} como {tipo}"}
