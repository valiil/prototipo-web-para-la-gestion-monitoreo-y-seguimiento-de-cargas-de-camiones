from pydantic import BaseModel
from datetime import date

class Envio(BaseModel):
    id_carga: int
    id_empresa: int
    id_transportador: int
   
