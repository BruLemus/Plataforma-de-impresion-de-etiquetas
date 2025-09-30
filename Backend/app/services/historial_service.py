from sqlalchemy.orm import Session
from sqlalchemy import literal
from app.db.models.tarima import Tarima
from app.db.models.caja import Caja
from app.db.models.user_coordinador import UserCoordinador
from app.db.models.user_practicante import UserPracticante

def obtener_historial(db: Session):
    # Tarimas
    tarimas_query = (
        db.query(
            (UserCoordinador.nombre).label("usuario"),
            literal("Coordinador").label("tipo_usuario"),
            Tarima.numero_factura,
            Tarima.cantidad_piezas,
            Tarima.tipo_embalaje,
            literal("Tarima").label("tipo_pedido"),
            Tarima.paqueteria,
            Tarima.clave_producto,
            Tarima.fecha_creacion
        )
        .join(UserCoordinador, Tarima.coordinador_id == UserCoordinador.id, isouter=True)
        .join(UserPracticante, Tarima.practicante_id == UserPracticante.user_id, isouter=True)
    )

    # Cajas
    cajas_query = (
        db.query(
            (UserCoordinador.nombre).label("usuario"),
            literal("Coordinador").label("tipo_usuario"),
            Caja.numero_factura,
            Caja.cantidad_piezas,
            Caja.tipo_embalaje,
            literal("Caja").label("tipo_pedido"),
            Caja.paqueteria,
            Caja.clave_producto,
            Caja.fecha_creacion
        )
        .join(UserCoordinador, Caja.coordinador_id == UserCoordinador.id, isouter=True)
        .join(UserPracticante, Caja.practicante_id == UserPracticante.user_id, isouter=True)
    )

    historial = tarimas_query.union_all(cajas_query).all()
    return historial
