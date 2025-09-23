from app.api.routes import caja
from app.db import database
from app.api.routes import caja as caja  # para registrar tablas
from app.api.routes import tarima
from app.api.routes import user_practicante
from app.api.routes import user_coordinador
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import imprimir
from pydantic import BaseModel
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
app.include_router(imprimir.router)

# ========= Servidor de impresión integrado =========
class PrintPayload(BaseModel):
    content: str

@app.post("/print_label/")
def print_label(payload: PrintPayload):
    try:
        # Nombre de impresora predeterminada en Windows
        printer_name = win32print.GetDefaultPrinter()

        # Abrir impresora
        hPrinter = win32print.OpenPrinter(printer_name)
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(printer_name)

        # Documento de impresión
        hDC.StartDoc("Etiqueta de envío")
        hDC.StartPage()

        # Dibujar el texto
        hDC.TextOut(100, 100, payload.content)

        # Finalizar impresión
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
