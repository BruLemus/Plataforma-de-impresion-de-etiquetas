from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.user_coordinador import UserCoordinador
from app.schemas.user_coordinador import UserCoordinadorUpdate, UserCoordinadorResponse
from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "SUPER_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_coordinator(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    user = db.query(UserCoordinador).filter(UserCoordinador.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    return user

# ---------------------------
# Perfil coordinador
# ---------------------------
@router.get("/perfil", response_model=UserCoordinadorResponse)
def get_perfil(current_user: UserCoordinador = Depends(get_current_coordinator)):
    return current_user

@router.put("/perfil", response_model=UserCoordinadorResponse)
def update_perfil(
    payload: UserCoordinadorUpdate,
    db: Session = Depends(get_db),
    current_user: UserCoordinador = Depends(get_current_coordinator)
):
    # Verificar código secreto
    if payload.codigo_secreto != current_user.codigo_secreto:
        raise HTTPException(status_code=403, detail="Código secreto inválido")

    if payload.nombre:
        current_user.nombre = payload.nombre
    if payload.contrasena:
        current_user.contrasena = pwd_context.hash(payload.contrasena)

    db.commit()
    db.refresh(current_user)
    return current_user
