# app/api/routes/imprimir.py
from fastapi import APIRouter, HTTPException
import socket
import time

router = APIRouter()

PRINTER_IP = "192.168.47.56:5000"  
PRINTER_PORT = 19200

def send_to_printer(data: bytes):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect((PRINTER_IP, PRINTER_PORT))
        s.sendall(data)
    finally:
        s.close()


@router.post("/print_batch/")
async def print_batch(payload: dict):
    """
    payload expected: {"labels": ["zpl or text 1", "zpl or text 2", ...]}
    Each label must be proper ZPL or raw printable data the Zebra understands.
    """
    labels = payload.get("labels")
    if not labels or not isinstance(labels, list):
        raise HTTPException(status_code=400, detail="labels debe ser una lista")

    try:
        for idx, lab in enumerate(labels):
            # Aquí asumo que 'lab' ya es ZPL o texto apropiado.
            # Asegúrate de incluir terminadores (ej. ^XZ) si es ZPL.
            data = lab.encode('utf-8')
            send_to_printer(data)
            # pequeño delay para que la impresora procese y acepte siguiente
            time.sleep(0.3)
        return {"status": "ok", "printed": len(labels)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
