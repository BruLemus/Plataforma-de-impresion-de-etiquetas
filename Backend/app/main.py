
from app.db import database
from app.api.routes import caja as caja  # para registrar tablas
from app.api.routes import tarima
from app.api.routes import user_practicante
from app.api.routes import user_coordinador
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.api.routes import caja
from app.api.routes import registro

import win32print
import win32ui

app = FastAPI(title="API de Etiquetas - Cajas")

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas (ejecuta esto al inicio, solo para desarrollo)
database.Base.metadata.create_all(bind=database.engine)

# Routers
app.include_router(caja.router, prefix="/cajas", tags=["Cajas"])
app.include_router(tarima.router, prefix="/tarimas", tags=["Tarimas"])
app.include_router(user_practicante.router, prefix="/user_practicantes", tags=["Usuarios Practicantes"])
app.include_router(user_coordinador.router, prefix="/user_coordinadors", tags=["Usuarios Coordinadores"])
app.include_router(registro.router, prefix="/historial", tags=["Registros"])

# ========= Servidor de impresión integrado =========
class PrintPayload(BaseModel):
    content: str
    use_zpl: bool = False  # Si es True, envía ZPL directo a Zebra

@app.post("/print_label/")
def print_label(payload: PrintPayload):
    try:
        # Nombre de impresora predeterminada en Windows
        printer_name = win32print.GetDefaultPrinter()

        if payload.use_zpl:
            # ===== Impresión RAW ZPL =====
            hPrinter = win32print.OpenPrinter(printer_name)
            try:
                hJob = win32print.StartDocPrinter(hPrinter, 1, ("Etiqueta", None, "RAW"))
                win32print.StartPagePrinter(hPrinter)
                win32print.WritePrinter(hPrinter, payload.content.encode())
                win32print.EndPagePrinter(hPrinter)
                win32print.EndDocPrinter(hPrinter)
            finally:
                win32print.ClosePrinter(hPrinter)
        else:
            # ===== Impresión tradicional con texto =====
            hPrinter = win32print.OpenPrinter(printer_name)
            hDC = win32ui.CreateDC()
            hDC.CreatePrinterDC(printer_name)
            hDC.StartDoc("Etiqueta de envío")
            hDC.StartPage()
            hDC.TextOut(100, 100, payload.content)
            hDC.EndPage()
            hDC.EndDoc()
            hDC.DeleteDC()
            win32print.ClosePrinter(hPrinter)

        return {"status": "ok", "message": f"Etiqueta enviada a {printer_name}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ========= Root =========
@app.get("/")
def root():
    return {"message": "API lista. Revisa /docs para interactuar."}


@app.get("/print_label/status")
def printer_status():
    try:
        printer_name = win32print.GetDefaultPrinter()
        printers = [p[2] for p in win32print.EnumPrinters(2)]
        online = printer_name in printers
        return {"online": online, "printer_name": printer_name}
    except Exception:
        return {"online": False, "printer_name": None}

