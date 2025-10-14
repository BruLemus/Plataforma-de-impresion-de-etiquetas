from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models.tarima_mx import Tarima_mx
from app.schemas.tarima_mx import TarimaMXCreate
from app.db.models.user_coordinador_mx import UserCoordinadorMX
from app.db.models.user_practicante_mx import UserPracticanteMX


def create_tarima_mx(db: Session, payload: TarimaMXCreate, current_user) -> Tarima_mx:
    """
    Crea una tarima MX y asigna coordinador o practicante según el rol del usuario logueado.
    current_user: objeto UserCoordinadorMX o UserPracticanteMX
    """
    db_tarima = Tarima_mx(
        numero_facturas=payload.numero_facturas,
        numero_tarimas=payload.numero_tarimas,
        tipo_embalaje=payload.tipo_embalaje,
        paqueteria=payload.paqueteria,
        clave_producto=payload.clave_producto,
        cantidad_piezas=payload.cantidad_piezas or 0,
        ancho=payload.ancho or 0,
        alto=payload.alto or 0,
        largo=payload.largo or 0,
        peso=payload.peso or 0,
        peso_volumetrico=payload.peso_volumetrico or None,
        nombre_user_coordinador=current_user.nombre if isinstance(current_user, UserCoordinadorMX) else None,
        nombre_user_practicante=current_user.nombre if isinstance(current_user, UserPracticanteMX) else None,
        coordinador_id=current_user.id if isinstance(current_user, UserCoordinadorMX) else None,
        practicante_id=current_user.user_id if isinstance(current_user, UserPracticanteMX) else None,
    )
    db.add(db_tarima)
    db.commit()
    db.refresh(db_tarima)
    return db_tarima


def get_tarimas_mx(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    paqueteria: Optional[str] = None,
    numero_facturas: Optional[str] = None,
    current_user=None
) -> List[Tarima_mx]:
    """
    Lista tarimas MX, opcionalmente filtradas por paquetería, factura o usuario logueado.
    current_user: objeto UserCoordinadorMX o UserPracticanteMX
    """
    query = db.query(Tarima_mx)

    if paqueteria:
        query = query.filter(Tarima_mx.paqueteria == paqueteria)
    if numero_facturas:
        query = query.filter(Tarima_mx.numero_facturas == numero_facturas)

    # Filtrar por rol si se pasa current_user
    if current_user:
        if isinstance(current_user, UserCoordinadorMX):
            query = query.filter(Tarima_mx.coordinador_id == current_user.id)
        elif isinstance(current_user, UserPracticanteMX):
            query = query.filter(Tarima_mx.practicante_id == current_user.user_id)

    return query.offset(skip).limit(limit).all()


def get_tarima_mx_by_id(db: Session, tarima_id: int) -> Optional[Tarima_mx]:
    """
    Obtiene una tarima MX por su ID.
    """
    return db.query(Tarima_mx).filter(Tarima_mx.id == tarima_id).first()


def update_tarima_mx(db: Session, tarima_id: int, payload: dict) -> Optional[Tarima_mx]:
    """
    Actualiza una tarima MX existente.
    """
    db_tarima = db.query(Tarima_mx).filter(Tarima_mx.id == tarima_id).first()
    if not db_tarima:
        return None

    for key, value in payload.items():
        setattr(db_tarima, key, value)

    db.commit()
    db.refresh(db_tarima)
    return db_tarima


def delete_tarima_mx(db: Session, tarima_id: int) -> bool:
    """
    Elimina una tarima MX por su ID.
    """
    db_tarima = db.query(Tarima_mx).filter(Tarima_mx.id == tarima_id).first()
    if not db_tarima:
        return False
    db.delete(db_tarima)
    db.commit()
    return True
