from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.database import SessionLocal
from app.schemas.user_practicante import UserPracticanteCreate, UserPracticanteUpdate
from app.schemas.user_practicante import UserPracticanteResponse
from app.services import user_practicante
from app.db.database import get_db



router = APIRouter()


        
@router.post("/", response_model=UserPracticanteResponse)
def create_user_practicante_endpoint(payload: UserPracticanteCreate, db: Session = Depends(get_db)):
    return user_practicante.create_user_practicante(db, payload)

@router.get("/", response_model=List[UserPracticanteResponse])
def list_user_practicantes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_practicante.get_user_practicantes(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserPracticanteResponse)
def get_user_practicante(user_id: int, db: Session = Depends(get_db)):
    db_user = user_practicante.get_user_practicante_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario practicante no encontrado")
    return db_user

@router.put("/{user_id}", response_model=UserPracticanteResponse)
def update_user_practicante_endpoint(user_id: int, payload: UserPracticanteUpdate, db: Session = Depends(get_db)):
    db_user = user_practicante.update_user_practicante(db, user_id, payload)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario practicante no encontrado")
    return db_user

@router.delete("/{user_id}")
def delete_user_practicante_endpoint(user_id: int, db: Session = Depends(get_db)):
    deleted = user_practicante.delete_user_practicante(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuario practicante no encontrado")
    return {"detail": "Usuario practicante eliminado correctamente"}
