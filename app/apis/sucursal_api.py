# app/apis/sucursal_api.py
from fastapi import APIRouter, HTTPException
from app.services.sucursal_service import (
    create_sucursal,
    get_sucursales,
    get_sucursal
)
from app.models.sucursal import SucursalCreate

router = APIRouter()

@router.post("/", response_model=dict)
async def create_new_sucursal(sucursal: SucursalCreate):
    return await create_sucursal(sucursal)  # Asegúrate de que estás pasando el modelo correctamente

@router.get("/", response_model=list)
async def list_sucursales():
    return await get_sucursales()

@router.get("/{sucursal_id}", response_model=dict)
async def retrieve_sucursal(sucursal_id: str):
    return await get_sucursal(sucursal_id)

@router.delete("/{sucursal_id}", response_model=dict)
async def remove_sucursal(sucursal_id: str):
    return await delete_sucursal(sucursal_id)