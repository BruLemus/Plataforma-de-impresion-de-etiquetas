from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models.tarima import Tarima
from app.schemas.tarima import TarimaCreate
from app.db.models.user_coordinador import UserCoordinador
from app.db.models.user_practicante import UserPracticante
from app.db.models.enums import PaqueteriaEnum


# -----------------------------
# CREAR TARIMA CON USUARIO LOGUEADO
# -----------------------------
def create_tarima(db: Session, payload: TarimaCreate, current_user) -> Tarima:
    # Calcular peso volumétrico solo para Estafeta y Paquetexpress
    peso_vol = 0
    if payload.paqueteria in [PaqueteriaEnum.ESTAFETA, PaqueteriaEnum.PAQUETEXPRESS, PaqueteriaEnum.FEDEX, PaqueteriaEnum.DHL,  PaqueteriaEnum.UPS, PaqueteriaEnum.MERCADO_LIBRE]:
        peso_vol = (payload.largo * payload.ancho * payload.alto) / 5000

    coordinador_id = current_user.id if hasattr(current_user, "id") and current_user.__class__.__name__ == "UserCoordinador" else None
    practicante_id = current_user.user_id if hasattr(current_user, "user_id") and current_user.__class__.__name__ == "UserPracticante" else None
    nombre_creador = current_user.nombre if hasattr(current_user, "nombre") else "Desconocido"

    db_tarima = Tarima(
        numero_facturas=payload.numero_facturas,
        numero_tarimas=payload.numero_tarimas,
        tipo_embalaje=payload.tipo_embalaje,
        paqueteria=payload.paqueteria,
        clave_producto=payload.clave_producto,
        cantidad_piezas=payload.cantidad_piezas or 0,
        ancho=payload.ancho,
        largo=payload.largo,
        alto=payload.alto,
        peso=payload.peso,
        peso_volumetrico=peso_vol,
        coordinador_id=coordinador_id,
        practicante_id=practicante_id,
        nombre_creador=nombre_creador
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
