from fastapi import APIRouter, HTTPException
from controllers.cargaTransportador_controller import CargaTransportadorController
from typing import Optional

router = APIRouter()
carga_transportador_controller = CargaTransportadorController()

@router.get("/cargas/transportador/{transportador_id}")
async def get_cargas_por_transportador(transportador_id: int, start_date: Optional[str] = None, end_date: Optional[str] = None):
    return carga_transportador_controller.get_cargas_por_transportador(transportador_id, start_date, end_date)
