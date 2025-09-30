from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models.user_coordinador import UserCoordinador
from app.schemas.user_coordinador import UserCoordinadorCreate, UserCoordinadorResponse
from typing import List
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
import jwt, datetime
from fastapi import Form
from jose import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Header
from fastapi import APIRouter, HTTPException
from fastapi import APIRouter, HTTPException
from app.schemas.user_coordinador import UserCoordinadorUpdate
from jose import jwt, JWTError
from app.db.database import get_db




router = APIRouter()



# ---------------------------
# Seguridad y Hash
# ---------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_CODE = "UPPER"  # Código para registrar coordinadores
SECRET_KEY = "SUPER_SECRET_KEY"  # Clave JWT (usar distinta en producción)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

token = "TU_TOKEN_AQUI"

security = HTTPBearer()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_coordinator(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(UserCoordinador).filter(UserCoordinador.nombre == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    return user


# ---------------------------
# Endpoint actualizado
# ---------------------------
@router.put("/perfil", response_model=UserCoordinadorResponse)
def update_perfil(
    payload: UserCoordinadorUpdate,
    db: Session = Depends(get_db),
    current_user: UserCoordinador = Depends(get_current_coordinator)
):
    # Verificar código secreto
    if payload.codigo_secreto != current_user.codigo_secreto:
        raise HTTPException(status_code=403, detail="Código secreto inválido")

    # Actualizar campos si se proporcionan
    if payload.nombre:
        current_user.nombre = payload.nombre

    if payload.contrasena:
        hashed_password = pwd_context.hash(payload.contrasena)
        current_user.contrasena = hashed_password

    db.commit()
    db.refresh(current_user)

    return current_user



def get_current_user(token: str = Header(...), db: Session = Depends(get_db)):
    # En un caso real, aquí validarías un JWT
    user = db.query(UserCoordinador).filter(UserCoordinador.id == token.replace("token_demo_", "")).first()
    if not user:
        raise HTTPException(status_code=401, detail="No autorizado")
    return user

@router.get("/dashboard")
def get_dashboard(current_user: UserCoordinador = Depends(get_current_user)):
    return {"msg": f"Hola {current_user.nombre}, este endpoint está protegido"}


# Login de coordinador
@router.post("/login", response_model=UserCoordinadorResponse)
def login_coordinador(nombre: str = Form(...), contrasena: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(UserCoordinador).filter(UserCoordinador.nombre == nombre).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    if not pwd_context.verify(contrasena, user.contrasena):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    # Generamos un token simple (por ejemplo JWT)
    token = create_token({"user_id": user.id})
    return {"nombre": user.nombre, "codigo_secreto": user.codigo_secreto, "id": user.id, "token": token}


# ---------------------------
# Endpoints
# ---------------------------

# Listar todos los coordinadores
@router.get("/", response_model=List[UserCoordinadorResponse])
def get_all_coordinadores(db: Session = Depends(get_db)):
    return db.query(UserCoordinador).all()


def create_token(data: dict, expires_delta: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


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

# Login coordinador
@router.post("/login")
def login_coordinador(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserCoordinador).filter(UserCoordinador.nombre == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    if not verify_password(form_data.password, user.contrasena):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    token = create_access_token(data={"sub": user.nombre})
    return {"nombre": user.nombre, "token": token}

# Eliminar coordinador por ID
@router.delete("/{coordinador_id}")
def delete_coordinador(coordinador_id: int, db: Session = Depends(get_db)):
    user = db.query(UserCoordinador).filter(UserCoordinador.id == coordinador_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Coordinador no encontrado")
    db.delete(user)
    db.commit()
    return {"detail": "Coordinador eliminado"}

# Endpoint protegido de prueba
@router.get("/me")
def get_me(current_user: UserCoordinador = Depends(get_current_coordinator)):
    return {"nombre": current_user.nombre, "id": current_user.id}
