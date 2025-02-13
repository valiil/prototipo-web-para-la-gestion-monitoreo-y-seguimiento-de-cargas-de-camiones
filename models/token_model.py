from pydantic import BaseModel

class Token_user(BaseModel):
    Usuario: str
    contrasena: str


class Token(BaseModel):
    token: str