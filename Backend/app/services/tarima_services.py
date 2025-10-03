from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models.tarima import Tarima
from app.schemas.tarima import TarimaCreate
from app.db.models.user_coordinador import UserCoordinador
from app.db.models.user_practicante import UserPracticante


# -----------------------------
# CREAR TARIMA CON USUARIO LOGUEADO
# -----------------------------
def create_tarima(db: Session, payload: TarimaCreate, current_user) -> Tarima:
    db_tarima = Tarima(
        paqueteria=payload.paqueteria,
        numero_factura=payload.numero_factura,
        tipo_embalaje=payload.tipo_embalaje,
        numero_tarimas=payload.numero_tarimas,
        cantidad_piezas=payload.cantidad_piezas,
        clave_producto=payload.clave_producto,
        ancho=payload.ancho or 0,
        alto=payload.alto or 0,
        largo=payload.largo or 0,
        peso=payload.peso or 0,
        coordinador_nombre=current_user.nombre if isinstance(current_user, UserCoordinador) else None,
        practicante_nombre=current_user.nombre if isinstance(current_user, UserPracticante) else None,
    )
    db.add(db_tarima)
    db.commit()
    db.refresh(db_tarima)
    return db_tarima


# -----------------------------
# OBTENER LISTA DE TARIMAS
# -----------------------------
def get_tarimas(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    paqueteria: Optional[str] = None,
    numero_factura: Optional[str] = None,
    current_user=None
) -> List[Tarima]:
    """
    Lista tarimas, opcionalmente filtradas por paquetería, factura o usuario logueado.
    current_user: objeto UserCoordinador o UserPracticante
    """
    query = db.query(Tarima)

    if paqueteria:
        query = query.filter(Tarima.paqueteria == paqueteria)
    if numero_factura:
        query = query.filter(Tarima.numero_factura == numero_factura)

    # Filtrar por rol si se pasa current_user
    if current_user:
        if isinstance(current_user, UserCoordinador):
            query = query.filter(Tarima.coordinador_nombre == current_user.nombre)
        elif isinstance(current_user, UserPracticante):
            query = query.filter(Tarima.practicante_nombre == current_user.nombre)

    return query.offset(skip).limit(limit).all()


# -----------------------------
# OBTENER TARIMA POR ID
# -----------------------------
def get_tarima_by_id(db: Session, tarima_id: int) -> Optional[Tarima]:
    return db.query(Tarima).filter(Tarima.tarima_id == tarima_id).first()


# -----------------------------
# ACTUALIZAR TARIMA
# -----------------------------
def update_tarima(db: Session, tarima_id: int, payload: TarimaCreate) -> Optional[Tarima]:
    db_tarima = get_tarima_by_id(db, tarima_id)
    if not db_tarima:
        return None
    for key, value in payload.dict().items():
        setattr(db_tarima, key, value)
    db.commit()
    db.refresh(db_tarima)
    return db_tarima


# -----------------------------
# ELIMINAR TARIMA
# -----------------------------
def delete_tarima(db: Session, tarima_id: int) -> bool:
    db_tarima = get_tarima_by_id(db, tarima_id)
    if not db_tarima:
        return False
    db.delete(db_tarima)
    db.commit()
    return True
