from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Security, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.database import get_db

# 🔹 Importa todos los modelos de usuarios (GDL y MX)
from app.db.models.user_coordinador import UserCoordinador  # Guadalajara
from app.db.models.user_coordinador_mx import UserCoordinadorMX  # México
from app.db.models.user_practicante import UserPracticante  # Guadalajara
from app.db.models.user_practicante_mx import UserPracticanteMX  # México


# ==========================================================
# 🔹 Configuración de seguridad
# ==========================================================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "SUPER_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 720  # 12 horas

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
    data: Diccionario con información del usuario (ej. {"id": id, "tipo": "coordinador", "region": "mx"})
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ==========================================================
# 🔹 Obtener usuario actual (automático según tipo y región)
# ==========================================================
def get_current_user(
    token: str = Header(...),  # Header personalizado: token: <JWT>
    db: Session = Depends(get_db)
):
    """
    Valida el token JWT y obtiene al usuario correspondiente según:
    - tipo: coordinador / practicante
    - region: gdl / mx
    """
    if not token:
        raise HTTPException(status_code=401, detail="Token requerido")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("id")
        tipo = payload.get("tipo")
        region = payload.get("region", "gdl")  # Por defecto Guadalajara

        if not id or not tipo:
            raise HTTPException(status_code=401, detail="Token inválido")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    # =====================================
    # 🔸 Coordinadores
    # =====================================
    if tipo == "coordinador":
        if region.lower() == "mx":
            user = db.query(UserCoordinadorMX).filter(UserCoordinadorMX.id == id).first()
        else:
            user = db.query(UserCoordinador).filter(UserCoordinador.id == id).first()

        if not user:
            raise HTTPException(status_code=401, detail="Usuario coordinador no encontrado")
        return user

    # =====================================
    # 🔸 Practicantes
    # =====================================
    elif tipo == "practicante":
        if region.lower() == "mx":
            user = db.query(UserPracticanteMX).filter(UserPracticanteMX.id == id).first()
        else:
            user = db.query(UserPracticante).filter(UserPracticante.id == id).first()

        if not user:
            raise HTTPException(status_code=401, detail="Usuario practicante no encontrado")
        return user

    # =====================================
    # ❌ Rol inválido
    # =====================================
    else:
        raise HTTPException(status_code=400, detail="Tipo de usuario no válido (usa 'coordinador' o 'practicante')")
