# routers/user_coordinador.py
from fastapi import APIRouter, Depends, HTTPException, Security, Form
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.user_coordinador import UserCoordinador
from app.schemas.user_coordinador import UserCoordinadorCreate, UserCoordinadorUpdate, UserCoordinadorResponse
from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import List
from fastapi import Header

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

def get_current_coordinator(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(UserCoordinador).filter(UserCoordinador.nombre == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user

# ---------------------------
# Endpoints Coordinador
# ---------------------------

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

@router.post("/login")
def login_coordinador(
    nombre: str = Form(...),
    contrasena: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(UserCoordinador).filter(UserCoordinador.nombre == nombre).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    if not verify_password(contrasena, user.contrasena):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # 🔹 Incluir datos completos dentro del token
    token = create_access_token({
        "sub": user.nombre,
        "user_id": user.id,
        "tipo": "coordinador"
    })

    return {
        "nombre": user.nombre,
        "id": user.id,
        "codigo_secreto": user.codigo_secreto,
        "token": token
    }



# Listar todos los coordinadores (opcional)
@router.get("/", response_model=List[UserCoordinadorResponse])
def get_all_coordinadores(db: Session = Depends(get_db)):
    return db.query(UserCoordinador).all()

# Eliminar coordinador por ID (sin token)
@router.delete("/{coordinador_id}")
def delete_coordinador(coordinador_id: int, db: Session = Depends(get_db)):
    user = db.query(UserCoordinador).filter(UserCoordinador.id == coordinador_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Coordinador no encontrado")
    db.delete(user)
    db.commit()
    return {"detail": "Coordinador eliminado"}
