from  fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.user_rol import UserRolCreate, UserRolRead
from typing import Optional, List
from app.services import user_rol_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Crear user_rol
@router.post("/", response_model=UserRolRead)
def create_user_rol(user_rol: UserRolCreate, db: Session = Depends(get_db)):
    return user_rol_service.create_user_rol(db=db, user_rol=user_rol)


# ✅ Listar user_rols con filtros opcionales
@router.get("/", response_model=List[UserRolRead])
def list_user_rols(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = Query(None, description="ID del usuario para filtrar"),
    rol_id: Optional[int] = Query(None, description="ID del rol para filtrar"),
    db: Session = Depends(get_db)
):
    return user_rol_service.get_user_rols(db, skip=skip, limit=limit, user_id=user_id, rol_id=rol_id)


# ✅ Obtener user_rol por ID
@router.get("/{user_rol_id}", response_model=UserRolRead)
def get_user_rol(user_rol_id: int, db: Session = Depends(get_db)):
    db_user_rol = user_rol_service.get_user_rol_by_id(db, user_rol_id)
    if not db_user_rol:
        raise HTTPException(status_code=404, detail="UserRol no encontrado")
    return db_user_rol

# ✅ Actualizar user_rol
@router.put("/{user_rol_id}", response_model=UserRolRead)
def update_user_rol(user_rol_id: int, user_rol: UserRolCreate, db: Session = Depends(get_db)):
    db_user_rol = user_rol_service.update_user_rol(db, user_rol_id, user_rol)
    if not db_user_rol:
        raise HTTPException(status_code=404, detail="UserRol no encontrado")
    return db_user_rol

# ✅ Eliminar user_rol
@router.delete("/{user_rol_id}")
def delete_user_rol(user_rol_id: int, db: Session = Depends(get_db)):
    deleted = user_rol_service.delete_user_rol(db, user_rol_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="UserRol no encontrado")
    return {"detail": "UserRol eliminado correctamente"}
