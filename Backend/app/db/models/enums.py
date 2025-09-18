# app/db/models/enums.py
from enum import Enum

class PaqueteriaEnum(str, Enum):
    PAQUETEXPRESS = "Paquetexpress"
    ESTAFETA = "Estafeta"
    DHL = "DHL"
    FEDEX = "FedEx"
    UPS = "UPS"
    MERCADO_LIBRE = "MercadoLibre"

class TipoEmbalajeEnum(int, Enum):
    TIPO1 = 1
    TIPO2 = 2
    TIPO3 = 3
    TIPO4 = 4
    TIPO5 = 5

class UserRoleEnum(str, Enum):
    Practicante = "Practicante"
    Coordinador = "Coordinador"
    
class mesaTrabajoEnum(str, Enum):
    MESA1 = "Mesa 1"
    MESA2 = "Mesa 2"
    MESA3 = "Mesa 3"
    MESA4 = "Mesa 4"
    MESA5 = "Mesa 5"
    MESA6 = "Mesa 6"
    MESA7 = "Mesa 7"
    MESA8 = "Mesa 8"
    MESA9 = "Mesa 9"
    MESA10 = "Mesa 10"
    
    


