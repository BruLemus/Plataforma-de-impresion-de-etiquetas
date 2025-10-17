# /app/routers/impresion.py

from fastapi import APIRouter
from pydantic import BaseModel, Field
import sys 
import json 

router = APIRouter() 

# **ATENCIÓN:** Esta clase LabelData debe coincidir con la que está en /app/models.py
class LabelData(BaseModel):
    """Define el esquema de datos completo para una etiqueta."""
    paqueteria: str
    factura: str
    num_cajas: int = Field(..., gt=0)
    caja_actual: int = Field(..., gt=0)
    piezas: int
    clave_producto: str = ""
    ancho: float = 0
    alto: float = 0
    largo: float = 0
    peso: float = 0
    peso_volumetrico: float = 0
    qr_data: str 

# --------------------------------------------------------------------------
# 1. FUNCIÓN GENERADORA ZPL (QR EMPUJADO A X=360)
# --------------------------------------------------------------------------
def generate_zpl_final_label(data: LabelData) -> str:
    """
    Genera el código ZPL, ajustando el QR a X=360 para empujarlo a la izquierda 
    y aumentar el margen derecho.
    """
    
    PAQUETERIAS_COMPLETAS = ["Estafeta", "Paquetexpress"]
    imprimir_completo = data.paqueteria in PAQUETERIAS_COMPLETAS
    
    print(f" 🔎 Generando ZPL (QR X=360) para Factura: {data.factura} | Completo: {imprimir_completo}") 
    
    zpl = "^XA"
    # Ancho y Largo de la etiqueta (77mm x 77mm @ 200 DPI = 606 puntos)
    zpl += "^MMT^PW606^LL606" 
    
    # --- CONTENIDO QR (Generado con NOMBRES DE CAMPOS) ---
    
    qr_data_list = []
    
    # 1. Paquetería, Factura, Tarima, Piezas (Siempre incluidos)
    qr_data_list.append(f"PAQUETERIA:{data.paqueteria}")
    qr_data_list.append(f"FACTURA:{data.factura}")
    qr_data_list.append(f"TARIMA:{data.caja_actual}_de_{data.num_cajas}")
    qr_data_list.append(f"PIEZAS:{data.piezas}")
    
    if imprimir_completo:
        # 2. Datos Condicionales (Dimensiones, Volumétrico, Peso)
        qr_data_list.append(f"DIMENSIONES:{data.ancho}x{data.alto}x{data.largo}cm")
        qr_data_list.append(f"VOLUMETRICO:{data.peso_volumetrico:.2f}kg")
        qr_data_list.append(f"PESO:{data.peso:.2f}kg")
        
    qr_content = "-".join(qr_data_list) 
    
    # --- DEFINICIÓN DE TAMAÑO Y POSICIÓN DEL QR ---
    
    # TAMAÑO: Si es completo (más datos), lo encogemos a 4; si no, usamos 5 para mejor lectura.
    qr_size = 4 if imprimir_completo else 5
    
    # POSICIÓN Y: Si es completo, lo subimos un poco (360); si no, puede estar más abajo (400).
    qr_y_position = 360 if imprimir_completo else 400
    
    # POSICIÓN X: AJUSTE PRINCIPAL: Recorrido a X=360 para empujar a la izquierda.
    qr_x_position = 360 
    
    # --- CABECERA ---
    
    # 1. Paquetería (GRANDE y CENTRADA - Fuente 50)
    zpl += "^CF0,50" 
    zpl += f"^FO23,20^FB560,1,0,C^FD{data.paqueteria.upper()}^FS"  
    
    # --- LÍNEA DIVISORA ---
    zpl += "^FO10,80^GB586,2,2^FS" 

    # 2. Tarima (EL MÁS GRANDE y CENTRADA - Fuente 80)
    zpl += "^CF0,80" 
    zpl += f"^FO23,100^FB560,1,0,C^FDTarima: {data.caja_actual} de {data.num_cajas}^FS" 
    
    # --- LÍNEA DIVISORA ---
    zpl += "^FO10,210^GB586,2,2^FS" 
    
    # 3. Factura (Fuente 30, alineada a la izquierda)
    zpl += "^CF0,30" 
    zpl += f"^FO20,230^FDFactura: {data.factura}^FS"
    
    # --- CONTENIDO INFERIOR (PIEZAS Y CONDICIONALES) ---
    
    y_current = 280
    
    # 4. Piezas (GRANDE - Fuente 35)
    zpl += "^CF0,35" 
    zpl += f"^FO20,{y_current}^FDPiezas: {data.piezas}^FS" 
    y_current += 40
    
    # --- BLOQUE CONDICIONAL (DIMENSIONES, VOLUMEN, PESO) ---
    
    if imprimir_completo:
        # Dimensiones (GRANDE - Fuente 35)
        zpl += "^CF0,35" 
        zpl += f"^FO20,{y_current}^FDDim (ANxALxL): {data.ancho}x{data.alto}x{data.largo} cm^FS"
        y_current += 40
        
        # Peso Volumétrico (GRANDE - Fuente 35)
        zpl += f"^FO20,{y_current}^FDVolumetrico: {data.peso_volumetrico:.2f} kg^FS"
        y_current += 40
        
        # Peso Real (GRANDE - Fuente 35)
        zpl += f"^FO20,{y_current}^FDPeso Real: {data.peso:.2f} kg^FS"
        
    # --- QR CODE (CONDICIONAL: TAMAÑO Y POSICIÓN) ---
    zpl += f"^FO{qr_x_position},{qr_y_position}^BQN,2,{qr_size}^FDQA,{qr_content}^FS"
    
    # --- FIN DE ETIQUETA ---
    zpl += "^PQ1"  # Imprime 1 copia
    zpl += "^XZ" 
    
    return zpl

# --------------------------------------------------------------------------
# 2. ENDPOINT DE FASTAPI (Sin cambios funcionales)
# --------------------------------------------------------------------------
@router.post("/generate")
def generate_zpl_for_client(data: list[LabelData]):
    """Genera el ZPL completo a partir de una lista de datos."""
    
    full_zpl_batch = ""
    
    if not data or len(data) == 0:
        print("🔴 INFO: La lista de datos de Vue llegó vacía.")
        return {"zpl_code": full_zpl_batch, "message": "No se recibieron datos."}
    
    print(f"✅ Recibidos {len(data)} cajas para procesar y generar ZPL.")
    
    try:
        # Itera sobre la lista y concatena el ZPL de cada etiqueta
        for i, label_data in enumerate(data):
            zpl_segment = generate_zpl_final_label(label_data) 
            full_zpl_batch += zpl_segment
            print(f"   Generada caja {i+1}. Longitud segmento: {len(zpl_segment)}")
            
    except Exception as e:
        print(f"🔴 ERROR FATAL AL CONCATENAR ZPL: {e}", file=sys.stderr)
        full_zpl_batch = ""
        return {"zpl_code": full_zpl_batch, "error": str(e)}, 500
    
    print(f"✅ ZPL final generado. Longitud total: {len(full_zpl_batch)}")
    
    return {"zpl_code": full_zpl_batch}