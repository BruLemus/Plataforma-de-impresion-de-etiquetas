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
    MESA1 = "1"
    MESA2 = "2"
    MESA3 = "3"
    MESA4 = "4"
    MESA5 = "5"
    MESA6 = "6"
    MESA7 = "7"
    MESA8 = "8"
    MESA9 = "9"
    MESA10 = "10"
    
    


