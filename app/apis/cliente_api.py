from fastapi import APIRouter, HTTPException
from app.services.cliente_service import create_cliente, get_clientes, get_cliente, delete_cliente, update_cliente_saldo, get_cliente_saldo, update_cliente_saldo
from app.models.cliente import ClienteCreate

router = APIRouter()

@router.post("/", response_model=dict)
async def create_new_cliente(cliente: ClienteCreate):
    return await create_cliente(cliente)

@router.get("/", response_model=list)
async def list_clientes():
    return await get_clientes()

@router.get("/{cliente_id}", response_model=dict)
async def retrieve_cliente(cliente_id: str):
    return await get_cliente(cliente_id)

@router.delete("/{cliente_id}", response_model=dict)
async def remove_cliente(cliente_id: str):
    return await delete_cliente(cliente_id)

# Endpoint para actualizar el saldo de un cliente
@router.put("/{cliente_id}/saldo", response_model=dict)
async def update_saldo_cliente(cliente_id: str, nuevo_saldo: int):  # Cambia a un parámetro de consulta
    await update_cliente_saldo(cliente_id, nuevo_saldo)
    return {"message": "Saldo actualizado con éxito", "cliente_id": cliente_id, "nuevo_saldo": nuevo_saldo}

# Nuevo endpoint para consultar el saldo de un cliente
@router.get("/{cliente_id}/saldo", response_model=dict)
async def get_saldo_cliente(cliente_id: str):
    saldo = await get_cliente_saldo(cliente_id)
    return {"cliente_id": cliente_id, "saldo": saldo}