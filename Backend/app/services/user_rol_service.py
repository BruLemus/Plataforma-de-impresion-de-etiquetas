#app/services/user_rol_service.py
from sqlalchemy.orm import Session
from app.db.models.user_rol import UserRol
from app.schemas.user_rol import UserRolCreate
from typing import List, Optional

def create_user_rol(db: Session, user_rol: UserRolCreate) -> UserRol:
    # pydantic -> dict -> SQLAlchemy constructor (enum types are compatibles)
    db_user_rol = UserRol(**user_rol.dict())
    db.add(db_user_rol)
    db.commit()
    db.refresh(db_user_rol)
    return db_user_rol  

def get_user_roles(db: Session, skip: int = 0, limit: int = 100, nombre: Optional[str] = None, UserRol: Optional[str] = None) -> List[UserRol]:
    query = db.query(UserRol)
    if nombre:
        query = query.filter(UserRol.nombre == nombre)
    if UserRol:
        query = query.filter(UserRol.UserRol == UserRol)
    return query.offset(skip).limit(limit).all()

def get_user_rol_by_id(db: Session, user_rol_id: int):
    return db.query(UserRol).filter(UserRol.user_rol_id == user_rol_id).first()

def delete_user_rol(db: Session, user_rol_id: int) -> bool:
    db_user_rol = db.query(UserRol).filter(UserRol.user_rol_id == user_rol_id).first()
    if db_user_rol:
        db.delete(db_user_rol)
        db.commit()
        return True
    return False

def update_user_rol(db: Session, user_rol_id: int, updated_data: dict) -> Optional[UserRol]:
    db_user_rol = db.query(UserRol).filter(UserRol.user_rol_id == user_rol_id).first()
    if db_user_rol:
        for key, value in updated_data.items():
            setattr(db_user_rol, key, value)
        db.commit()
        db.refresh(db_user_rol)
        return db_user_rol
    return None

