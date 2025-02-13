from fastapi import APIRouter
from controllers.envio_controller import EnvioController
from models.envio_model import Envio

router = APIRouter()

envio_controller = EnvioController()

@router.post("/create_envio")
async def create_envio(envio: Envio):
    return envio_controller.create_envio(envio)

@router.get("/get_envio/{envio_id}")
async def get_envio(envio_id: int):
    return envio_controller.get_envio(envio_id)

@router.get("/get_envios")
async def get_envios():
    return envio_controller.get_envios()

@router.put("/update_envio/{envio_id}")
async def update_envio(envio_id: int, envio: Envio):
    return envio_controller.update_envio(envio_id, envio)

@router.delete("/delete_envio/{envio_id}")
async def delete_envio(envio_id: int):
    return envio_controller.delete_envio(envio_id)
