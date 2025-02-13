from fastapi import APIRouter
from controllers.modulo_controller import ModuloController

router = APIRouter()

modulo_controller = ModuloController()

@router.get("/get_modulos/{perfil_id}")
async def get_modulos(perfil_id: int):
    return modulo_controller.get_modulos_por_perfil(perfil_id)

@router.patch("/actualizar_modulo/{modulo_id}/{perfil_id}/{estado}")
async def actualizar_modulo(modulo_id: int, perfil_id: int, estado: int):
    return modulo_controller.actualizar_estado_modulo(modulo_id, perfil_id, estado)

