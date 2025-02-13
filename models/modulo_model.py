from pydantic import BaseModel

class Modulo(BaseModel):
    id: int
    nombre: str
    descripcion: str
    activo: bool
