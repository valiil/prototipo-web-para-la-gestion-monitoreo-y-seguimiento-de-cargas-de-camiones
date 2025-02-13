from fastapi import APIRouter, HTTPException
from controllers.usuario_controller import UsuarioController
from models.usuario_model import Usuario

router = APIRouter()

nuevo_usuario = UsuarioController()

@router.post("/create_usuario")
async def create_usuario(usuario: Usuario):
    rpta = nuevo_usuario.create_usuario(usuario)
    return rpta

@router.get("/get_usuario/{usuario_id}", response_model=Usuario)
async def get_usuario(usuario_id: int):
    rpta = nuevo_usuario.get_usuario(usuario_id)
    return rpta

@router.get("/get_usuarios/")
async def get_usuarios():
    rpta = nuevo_usuario.get_usuarios()
    return rpta

@router.put("/update_usuario/{usuario_id}")
async def update_usuario(usuario_id: int, usuario: Usuario):
    rpta = nuevo_usuario.update_usuario(usuario_id, usuario)
    return rpta

@router.delete("/delete_usuario/{usuario_id}")
async def delete_usuario(usuario_id: int):
    rpta = nuevo_usuario.delete_usuario(usuario_id)
    
    if not rpta:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o ya inactivo")
    
    return {"message": "Usuario inactivado exitosamente"}
