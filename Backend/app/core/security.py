from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Security, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.user_coordinador import UserCoordinador
from app.db.models.user_practicante import UserPracticante

# 🔹 Configuración de seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "SUPER_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

security = HTTPBearer()

# 🔹 Funciones de hashing
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 🔹 Generación de JWT
def create_access_token(data: dict, expires_delta: int = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔹 Obtener usuario coordinador logueado
def get_current_coordinator(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(UserCoordinador).filter(UserCoordinador.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user

# 🔹 Obtener usuario coordinador o practicante logueado
def get_current_user(
    role: str,
    token: str = Header(None),  # Practicante no necesita token
    db: Session = Depends(get_db)
):
    """
    role: "coordinador" o "practicante"
    token: JWT enviado en header 'token' solo para coordinador
    """
    if role == "practicante":
        # Retorna un practicante "loggeado" sin token
        user = db.query(UserPracticante).first()  # Ajusta criterio real si hay más de uno
        if not user:
            raise HTTPException(status_code=401, detail="Practicante no encontrado")
        return user

    # Coordinador requiere token
    if not token:
        raise HTTPException(status_code=401, detail="Se requiere token para coordinador")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(UserCoordinador).filter(UserCoordinador.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario coordinador no encontrado")
    return user
