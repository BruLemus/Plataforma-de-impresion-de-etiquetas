from fastapi import APIRouter, Depends, HTTPException, Security, Form, Header
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta

from app.db.database import get_db
from app.db.models.user_coordinador_mx import UserCoordinadorMX
from app.schemas.user_coordinador_mx import (
    UserCoordinadorMXCreate,
    UserCoordinadorMXUpdate,
    UserCoordinadorMXResponse
)

router = APIRouter()

# ---------------------------
# Seguridad y Hash
# ---------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_CODE = "UPPER"  # Código para registrar coordinadores
SECRET_KEY = "SUPER_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

security = HTTPBearer()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_coordinator_mx(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(UserCoordinadorMX).filter(UserCoordinadorMX.nombre == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user


# ---------------------------
# Endpoints Coordinador MX
# ---------------------------


# Crear coordinador
@router.post("/", response_model=UserCoordinadorMXResponse)
def create_coordinador_mx(payload: UserCoordinadorMXCreate, db: Session = Depends(get_db)):
    if payload.codigo_secreto != SECRET_CODE:
        raise HTTPException(status_code=403, detail="Código secreto incorrecto")
    hashed_password = pwd_context.hash(payload.contrasena)
    user = UserCoordinadorMX(
        nombre=payload.nombre,
        contrasena=hashed_password,
        codigo_secreto=payload.codigo_secreto
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Login coordinador
@router.post("/login")
def login_coordinador_mx(
    nombre: str = Form(...),
    contrasena: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(UserCoordinadorMX).filter(UserCoordinadorMX.nombre == nombre).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    if not verify_password(contrasena, user.contrasena):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    token_data = {
        "id": user.id,
        "sub": user.nombre,
        "tipo": "coordinador"
    }
    token = create_access_token(token_data)
    
    return {
        "nombre": user.nombre,
        "id": user.id,
        "codigo_secreto": user.codigo_secreto,
        "token": token
    }

# Ver perfil (protegido)
@router.get("/me", response_model=UserCoordinadorMXResponse)
def get_me_mx(current_user: UserCoordinadorMX = Depends(get_current_coordinator_mx)):
    return current_user

# Actualizar perfil (protegido)
@router.put("/perfil", response_model=UserCoordinadorMXResponse)
def update_perfil_coordinador_mx(
    payload: UserCoordinadorMXUpdate,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = data.get("id")
        tipo = data.get("tipo", "").lower()
        if tipo != "coordinador":
            raise HTTPException(status_code=403, detail="No autorizado")
    except JWTError:
        raise HTTPException(status_code=401, detail="Inicia Sesión nuevamente")

    user = db.query(UserCoordinadorMX).filter(UserCoordinadorMX.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if payload.codigo_secreto != user.codigo_secreto:
        raise HTTPException(status_code=403, detail="Código secreto inválido")

    if payload.nombre:
        user.nombre = payload.nombre
    if payload.contrasena:
        user.contrasena = pwd_context.hash(payload.contrasena)

    db.commit()
    db.refresh(user)

    return user

# Listar todos los coordinadores
@router.get("/", response_model=List[UserCoordinadorMXResponse])
def get_all_coordinadores_mx(db: Session = Depends(get_db)):
    return db.query(UserCoordinadorMX).all()

# Eliminar coordinador por ID
@router.delete("/{coordinador_id}")
def delete_coordinador_mx(coordinador_id: int, db: Session = Depends(get_db)):
    user = db.query(UserCoordinadorMX).filter(UserCoordinadorMX.id == coordinador_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Coordinador no encontrado")
    db.delete(user)
    db.commit()
    return {"detail": "Coordinador eliminado"}
