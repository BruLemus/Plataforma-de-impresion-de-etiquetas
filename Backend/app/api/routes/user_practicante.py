# routers/user_practicante.py
from fastapi import APIRouter, Depends, HTTPException, Security, Form, Header
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.user_practicante import UserPracticante
from app.schemas.user_practicante import (
    UserPracticanteCreate, 
    UserPracticanteUpdate, 
    UserPracticanteResponse
)
from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import List

router = APIRouter()

# ---------------------------
# Seguridad y Hash
# ---------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
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

def get_current_practicante(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(UserPracticante).filter(UserPracticante.nombre == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user

# ---------------------------
# Endpoints Practicante
# ---------------------------

# Crear practicante
@router.post("/", response_model=UserPracticanteResponse)
def create_practicante(payload: UserPracticanteCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(payload.contrasena)
    user = UserPracticante(
        nombre=payload.nombre,
        contrasena=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Login practicante
@router.post("/login")
def login_practicante(
    nombre: str = Form(...),
    contrasena: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(UserPracticante).filter(UserPracticante.nombre == nombre).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    if not verify_password(contrasena, user.contrasena):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    token_data = {
        "user_id": user.user_id,      # 🔹 Cambiado de id a user_id
        "sub": user.nombre,
        "tipo": "practicante"
    }
    token = create_access_token(token_data)
    
    return {
        "nombre": user.nombre,
        "id": user.user_id,           # 🔹 Cambiado de id a user_id
        "token": token
    }

# Ver perfil (protegido)
@router.get("/me", response_model=UserPracticanteResponse)
def get_me(current_user: UserPracticante = Depends(get_current_practicante)):
    return current_user

# Actualizar perfil (protegido)
@router.put("/perfil", response_model=UserPracticanteResponse)
def update_perfil_practicante(
    payload: UserPracticanteUpdate,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = data.get("user_id")
        tipo = data.get("tipo", "").lower()
        if tipo != "practicante":
            raise HTTPException(status_code=403, detail="No autorizado")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    user = db.query(UserPracticante).filter(UserPracticante.user_id == user_id).first()  # 🔹 Cambiado
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if payload.nombre:
        user.nombre = payload.nombre
    if payload.contrasena:
        user.contrasena = pwd_context.hash(payload.contrasena)

    db.commit()
    db.refresh(user)

    return user

# Listar todos los practicantes
@router.get("/", response_model=List[UserPracticanteResponse])
def get_all_practicantes(db: Session = Depends(get_db)):
    return db.query(UserPracticante).all()

# Eliminar practicante por ID
@router.delete("/{practicante_id}")
def delete_practicante(practicante_id: int, db: Session = Depends(get_db)):
    user = db.query(UserPracticante).filter(UserPracticante.user_id == practicante_id).first()  # 🔹 Cambiado
    if not user:
        raise HTTPException(status_code=404, detail="Practicante no encontrado")
    db.delete(user)
    db.commit()
    return {"detail": "Practicante eliminado"}
