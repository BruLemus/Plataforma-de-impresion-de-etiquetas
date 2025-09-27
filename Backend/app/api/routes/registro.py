from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import caja, tarima, user_coordinador, user_practicante
from sqlalchemy import union_all
from sqlalchemy import asc


router = APIRouter()

@router.get("/historial")
def get_historial(db: Session = Depends(get_db)):
    # Consultar cajas
    query_cajas = (
        db.query(
            caja.numero_factura.label("numero_factura"),
            caja.paqueteria.label("paqueteria"),
            caja.cantidad_piezas.label("cantidad_piezas"),
            caja.clave_producto.label("clave_producto"),
            caja.tipo_embalaje.label("tipo_embalaje"),
            caja.fecha_creacion.label("fecha_creacion"),
            user_coordinador.nombre.label("usuario")
        )
        .join(user_coordinador, user_coordinador.id == caja.coordinador_id)
    )

    # Consultar tarimas
    query_tarimas = (
        db.query(
            tarima.numero_factura.label("numero_factura"),
            tarima.paqueteria.label("paqueteria"),
            tarima.cantidad_piezas.label("cantidad_piezas"),
            tarima.clave_producto.label("clave_producto"),
            tarima.tipo_embalaje.label("tipo_embalaje"),
            tarima.fecha_creacion.label("fecha_creacion"),
            user_practicante.nombre.label("usuario")
        )
        .join(user_practicante, user_practicante.id == tarima.practicante_id)
    )

    # Combinar con UNION ALL

    historial = query_cajas.union_all(query_tarimas).subquery()
    historial_query = db.query(historial).order_by(historial.c.fecha_creacion.asc()).all()

    # Convertir a lista de diccionarios para JSON
    result = [dict(r._mapping) for r in historial]
    return result
