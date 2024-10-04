from fastapi import APIRouter, HTTPException
from app.services.transaccion_service import registrar_transaccion, get_transacciones, cancelar_transaccion_servicio
from app.models.transaccion import TransaccionCreate, TransaccionResponse, CancelarTransaccionRequest
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=dict)
async def create_transaccion(transaccion: TransaccionCreate):
    return await registrar_transaccion(
        transaccion.cliente_id, 
        transaccion.producto_id, 
        transaccion.tipo, 
        transaccion.monto
    )

@router.get("/{cliente_id}", response_model=list)
async def historial_transacciones(cliente_id: str):
    return await get_transacciones(cliente_id)


   

@router.post("/cancelar", response_model=dict)
async def cancelar_transaccion(cancelar_data: CancelarTransaccionRequest):
    return await cancelar_transaccion_servicio(
        cancelar_data.id, 
        cancelar_data.cliente_id
    )