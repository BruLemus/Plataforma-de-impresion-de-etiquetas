from sqlalchemy.orm import Session
from app.db.models.user_practicante import UserPracticante
from app.schemas.user_practicante import UserPracticanteCreate, UserPracticanteUpdate
from typing import List, Optional

# 🔹 Crear usuario con contraseña hasheada
def create_user_practicante(db: Session, payload: UserPracticanteCreate) -> UserPracticante:
    db_user = UserPracticante(
        nombre=payload.nombre,
        mesa_trabajo=payload.mesa_trabajo,
    )
    db_user.set_password(payload.contrasena)  # 🔹 Hash de la contraseña
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_practicantes(db: Session, skip: int = 0, limit: int = 100) -> List[UserPracticante]:
    return db.query(UserPracticante).offset(skip).limit(limit).all()

def get_user_practicante_by_id(db: Session, user_id: int):
    return db.query(UserPracticante).filter(UserPracticante.user_id == user_id).first()


# 🔹 Actualizar usuario con contraseña opcional
def update_user_practicante(db: Session, user_id: int, payload: UserPracticanteUpdate) -> Optional[UserPracticante]:
    db_user = get_user_practicante_by_id(db, user_id)
    if not db_user:
        return None
    data = payload.dict(exclude_unset=True)  # solo actualizar campos enviados
    if "contrasena" in data and data["contrasena"]:
        db_user.set_password(data.pop("contrasena"))  # actualizar hash
    for key, value in data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user_practicante(db: Session, user_id: int) -> bool:
    db_user = get_user_practicante_by_id(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True
