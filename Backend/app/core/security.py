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
ACCESS_TOKEN_EXPIRE_MINUTES = 720  # Duración del token: 12 horas

security = HTTPBearer()

# ==========================================================
# 🔹 Funciones de hashing
# ==========================================================
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica que la contraseña en texto plano coincida con el hash."""
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """Genera el hash seguro de una contraseña."""
    return pwd_context.hash(password)


# ==========================================================
# 🔹 Generación de JWT
# ==========================================================
def create_access_token(data: dict, expires_delta: int = None) -> str:
    """
    Crea un token JWT con los datos del usuario.
    data: Diccionario con información del usuario (ej. {"user_id": id})
    expires_delta: Tiempo en minutos de expiración del token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ==========================================================
# 🔹 Obtener usuario coordinador logueado
# ==========================================================
def get_current_coordinator(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    """
    Valida el token del coordinador y retorna su información.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    user = db.query(UserCoordinador).filter(UserCoordinador.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario coordinador no encontrado")
    return user


# ==========================================================
# 🔹 Obtener usuario (coordinador o practicante) logueado
# ==========================================================
def get_current_user(
    role: str,
    token: str = Header(...),  # Se espera header "token: <JWT>"
    db: Session = Depends(get_db)
):
    """
    Verifica el token JWT y devuelve el usuario correspondiente según el rol.
    role: "coordinador" o "practicante"
    token: JWT enviado en el header 'token'
    """
    if not token:
        raise HTTPException(status_code=401, detail="Token requerido")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    if role == "coordinador":
        user = db.query(UserCoordinador).filter(UserCoordinador.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="Usuario coordinador no encontrado")
        return user

    elif role == "practicante":
        user = db.query(UserPracticante).filter(UserPracticante.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="Usuario practicante no encontrado")
        return user

    else:
        raise HTTPException(status_code=400, detail="Rol no válido (usa 'coordinador' o 'practicante')")
