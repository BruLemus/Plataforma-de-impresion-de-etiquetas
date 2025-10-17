from fastapi import APIRouter
from pydantic import BaseModel, Field
import sys 
import json 

router = APIRouter() 

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
    is_tarima: bool = False 


def generate_zpl_final_label(data: LabelData) -> str:
    """
    Genera el código ZPL, usando el campo is_tarima para ajustar el texto del encabezado,
    y el campo paqueteria para decidir el contenido (completo o básico).
    """
    
    PAQUETERIAS_COMPLETAS = ["Estafeta", "Paquetexpress"]
    imprimir_completo = data.paqueteria in PAQUETERIAS_COMPLETAS
    

    title_type = "TARIMA" if data.is_tarima else "CAJA"
    
    print(f" 🔎 Generando ZPL ({title_type} | QR Condicional) para Factura: {data.factura} | Completo: {imprimir_completo}") 
    
    zpl = "^XA"
    
    zpl += "^MMT^PW606^LL606" 
    
   
    
    qr_data_list = []
    
  
    qr_data_list.append(f"PAQUETERIA:{data.paqueteria}")
    qr_data_list.append(f"FACTURA:{data.factura}")
    qr_data_list.append(f"{title_type.upper()}:{data.caja_actual}_de_{data.num_cajas}") 
    qr_data_list.append(f"PIEZAS:{data.piezas}")
    
    if imprimir_completo:
        
        qr_data_list.append(f"DIMENSIONES:{data.ancho}x{data.alto}x{data.largo}cm")
        qr_data_list.append(f"VOLUMETRICO:{data.peso_volumetrico:.2f}kg")
        qr_data_list.append(f"PESO:{data.peso:.2f}kg")
        
    qr_content = "-".join(qr_data_list) 
    

    qr_size = 4 if imprimir_completo else 5
    qr_y_position = 360 if imprimir_completo else 400
    qr_x_position = 360 
    
   
    zpl += "^CF0,50" 
    zpl += f"^FO23,20^FB560,1,0,C^FD{data.paqueteria.upper()}^FS"  
    
    zpl += "^FO10,80^GB586,2,2^FS" 


    zpl += "^CF0,80" 
    zpl += f"^FO23,100^FB560,1,0,C^FD{title_type}: {data.caja_actual} de {data.num_cajas}^FS" 
    
    
    
    zpl += "^CF0,40" 
    zpl += f"^FO20,230^FDFactura: {data.factura}^FS"
    

    y_current = 280
    
  
    zpl += "^CF0,40" 
    zpl += f"^FO20,{y_current}^FDPiezas: {data.piezas}^FS"
    y_current += 45 
   
    if imprimir_completo:
      
        zpl += "^CF0,35" 
        zpl += f"^FO20,{y_current}^FDDims: {data.ancho}x{data.alto}x{data.largo} cm^FS"
        y_current += 40 
        
        
        zpl += "^CF0,35" 
        zpl += f"^FO20,{y_current}^FDPeso Real: {data.peso:.2f} kg^FS"
        y_current += 40 
     
        zpl += "^CF0,35" 
        zpl += f"^FO20,{y_current}^FDPeso Vol.: {data.peso_volumetrico:.2f} kg^FS"
        y_current += 40 
  
    zpl += f"^FO{qr_x_position},{qr_y_position}^BQN,2,{qr_size}^FDQA,{qr_content}^FS"
    
 
    zpl += "^PQ1" 
    zpl += "^XZ" 
    
    return zpl


@router.post("/generate_caja")
def generate_zpl_for_caja(data: list[LabelData]):
    """Genera el ZPL completo a partir de una lista de datos de Cajas."""
   
    for label in data:
        label.is_tarima = False
    
    return {"zpl_code": "".join(generate_zpl_final_label(label) for label in data)}


@router.post("/generate_tarima") 
def generate_zpl_for_tarima(data: list[LabelData]):

    for label in data:
        label.is_tarima = True
        
    return {"zpl_code": "".join(generate_zpl_final_label(label) for label in data)}