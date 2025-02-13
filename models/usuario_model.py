from pydantic import BaseModel

class Usuario(BaseModel):
    usuario: str
    contrasena: str
    nombre: str
    apellidos: str
    documento: str
    telefono: str
    id_perfil: int
    estado: str  

    