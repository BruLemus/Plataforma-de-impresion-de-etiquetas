from fastapi import APIRouter, Depends, HTTPException, Form, Header
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.user_coordinador_mx import UserCoordinadorMX
from app.db.models.user_practicante_mx import UserPracticanteMX
from app.db.models.user_coordinador import UserCoordinador
from app.db.models.user_practicante import UserPracticante
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
ACCESS_TOKEN_EXPIRE_MINUTES = 720  # 12 horas

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ---------------------------
# Login dinámico (ciudad + tipo)
# ---------------------------
@router.post("/login/{ciudad}/{tipo}/")
def login(
    ciudad: str,
    tipo: str,
    nombre: str = Form(...),
    contrasena: str = Form(...),
    db: Session = Depends(get_db)
):
    ciudad = ciudad.lower()
    tipo = tipo.lower()

    # Modelos dinámicos según ciudad y tipo
    if ciudad == "mexico":
        if tipo == "coordinador":
            model = UserCoordinadorMX
        elif tipo == "practicante":
            model = UserPracticanteMX
        else:
            raise HTTPException(status_code=400, detail="Tipo inválido para México")
    elif ciudad == "guadalajara":
        if tipo == "coordinador":
            model = UserCoordinador
        elif tipo == "practicante":
            model = UserPracticante
        else:
            raise HTTPException(status_code=400, detail="Tipo inválido para Guadalajara")
    else:
        raise HTTPException(status_code=400, detail="Ciudad inválida")

    # Buscar usuario
    user = db.query(model).filter(model.nombre == nombre).first()
    if not user or not verify_password(contrasena, user.contrasena):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    # Crear token
    token_data = {"user_id": user.id, "tipo": tipo, "ciudad": ciudad}
    token = create_access_token(token_data)

    return {"nombre": user.nombre, "token": token, "ciudad": ciudad, "tipo": tipo}


# ---------------------------
# Validación de token y dashboard
# ---------------------------
def get_current_user(ciudad: str, role: str, token: str = Header(...), db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Token requerido")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        token_role = payload.get("tipo")
        token_city = payload.get("ciudad")

        if not user_id or token_role != role or token_city != ciudad:
            raise HTTPException(status_code=401, detail="Token inválido o no autorizado")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    # Modelos dinámicos para verificación
    if ciudad == "mexico":
        model = UserCoordinadorMX if role == "coordinador" else UserPracticanteMX
    elif ciudad == "guadalajara":
        model = UserCoordinador if role == "coordinador" else UserPracticante
    else:
        raise HTTPException(status_code=400, detail="Ciudad inválida")

    user = db.query(model).filter(model.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail=f"{role.capitalize()} no encontrado")

    return user


@router.get("/dashboard/{ciudad}/{tipo}/")
def dashboard(ciudad: str, tipo: str, token: str = Header(...), db: Session = Depends(get_db)):
    user = get_current_user(ciudad, tipo, token, db)
    return {"msg": f"Bienvenido {user.nombre}, estás en el dashboard de {ciudad.capitalize()} como {tipo}"}
