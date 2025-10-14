from fastapi import APIRouter, Depends, HTTPException, Form, Header, Security
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta

from app.db.database import get_db
from app.db.models.user_practicante_mx import UserPracticanteMX
from app.schemas.user_practicante_mx import (
    UserPracticanteMXCreate,
    UserPracticanteMXUpdate,
    UserPracticanteMXResponse
)
from app.services.user_practicante_mx import (
    create_user_practicante_mx,
    get_user_practicantes_mx,
    get_user_practicante_mx_by_id,
    update_user_practicante_mx,
    delete_user_practicante_mx
)

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "SUPER_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
security = HTTPBearer()

def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_practicante_mx(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = db.query(UserPracticanteMX).filter(UserPracticanteMX.nombre == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user



# Crear practicante
@router.post("/", response_model=UserPracticanteMXResponse)
def create_practicante_mx(payload: UserPracticanteMXCreate, db: Session = Depends(get_db)):
    return create_user_practicante_mx(db, payload)

# Login practicante
@router.post("/login")
def login_practicante_mx(nombre: str = Form(...), contrasena: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(UserPracticanteMX).filter(UserPracticanteMX.nombre == nombre).first()
    if not user or not user.verify_password(contrasena):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    token = create_access_token({"id": user.id, "sub": user.nombre, "tipo": "practicante"})
    return {"nombre": user.nombre, "id": user.id, "token": token, "mesa_trabajo": user.mesa_trabajo}

# Ver perfil
@router.get("/me", response_model=UserPracticanteMXResponse)
def get_me_practicante_mx(current_user: UserPracticanteMX = Depends(get_current_practicante_mx)):
    return current_user

# Actualizar perfil
@router.put("/perfil", response_model=UserPracticanteMXResponse)
def update_perfil_practicante_mx(payload: UserPracticanteMXUpdate, token: str = Header(...), db: Session = Depends(get_db)):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = data.get("id")
        tipo = data.get("tipo", "").lower()
        if tipo != "practicante":
            raise HTTPException(status_code=403, detail="No autorizado")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = get_user_practicante_mx_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return update_user_practicante_mx(db, id, payload)

# Listar todos practicantes
@router.get("/", response_model=List[UserPracticanteMXResponse])
def get_all_practicantes_mx(db: Session = Depends(get_db)):
    return get_user_practicantes_mx(db)

# Eliminar practicante
@router.delete("/{practicante_id}")
def delete_practicante_mx(practicante_id: int, db: Session = Depends(get_db)):
    deleted = delete_user_practicante_mx(db, practicante_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Practicante no encontrado")
    return {"detail": "Practicante eliminado"}
