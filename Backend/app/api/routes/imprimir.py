from fastapi import APIRouter
from pydantic import BaseModel
import requests

router = APIRouter()

class ImpresionRequest(BaseModel):
    contenido: str

@router.post("/imprimir/")
def imprimir_directo(payload: ImpresionRequest):
    """
    Envía directamente a la impresora de red en 192.168.47.71:5000
    """
    try:
        # Suponiendo que la impresora recibe POST con texto plano
        resp = requests.post(
            "http://192.168.47.71:5000", 
            data=payload.contenido.encode("utf-8")
        )
        resp.raise_for_status()
        return {"status": "ok", "message": "Impresión enviada"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
