
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
from starlette.middleware.cors import CORSMiddleware 
import uvicorn
import win32print
import sys 



app = FastAPI()


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080", 
    "*" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

#  REEMPLAZA CON EL NOMBRE EXACTO DE TU IMPRESORA ZEBRA EN WINDOWS
PRINTER_NAME = "ZDesigner ZT230-200dpi ZPL" 



class PrintJob(BaseModel):
    """Define el esquema de datos esperado: solo la cadena ZPL."""
    zpl_code: str
    


def get_printer_status():
    """Verifica si la impresora existe y está lista."""
    try:
        printers = [p[2] for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)]
        if PRINTER_NAME not in printers:
            return {"status": "error", "message": f"Impresora '{PRINTER_NAME}' no encontrada en el sistema."}
        return {"status": "ok", "message": f"Impresora '{PRINTER_NAME}' lista para recibir trabajos."}
    except Exception as e:
        return {"status": "error", "message": f"Error al acceder a las impresoras (Spooler?): {e}"}

# -------------------- ENDPOINTS --------------------

@app.get("/status")
def status():
    """Verifica el estado del servicio local y la impresora."""
    return get_printer_status()

@app.post("/print")
def print_zpl_usb(job: PrintJob):
    """Recibe ZPL y lo envía a la impresora local en formato RAW."""
    
    if not job.zpl_code:
        raise HTTPException(status_code=400, detail="El código ZPL no puede estar vacío.")

    try:
       
        hPrinter = win32print.OpenPrinter(PRINTER_NAME)
        
        
        win32print.StartDocPrinter(hPrinter, 1, ("Etiqueta ZPL desde Web", None, "RAW"))
        
      
        win32print.WritePrinter(hPrinter, job.zpl_code.encode('utf-8'))
        
        
        win32print.EndDocPrinter(hPrinter)
        win32print.ClosePrinter(hPrinter)
        
        print(f"✅ Trabajo ZPL enviado a {PRINTER_NAME}. Longitud: {len(job.zpl_code)}")
        return {"status": "success", "message": "Impresión enviada correctamente al puerto USB."}
        
    except Exception as e:
        print(f"🔴 Error al imprimir en la USB: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Error de impresión: Revise el nombre exacto de la impresora o la conexión: {e}")

# -------------------- INICIO DEL SERVIDOR --------------------

if __name__ == "__main__":
    print(f"--- 🚀 Iniciando Micro-servicio Local ---")
    print(f"   URL de servicio: http://127.0.0.1:8001")
    
    status_check = get_printer_status()
    print(f"   Estado de Impresora: {status_check['message']}")
    
 
    uvicorn.run(app, host="127.0.0.1", port=8001)