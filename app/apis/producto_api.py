# app/apis/producto_api.py
from fastapi import APIRouter, HTTPException
from app.services.producto_service import (
    create_producto,
    get_productos,
    get_producto
)
from app.models.productos import ProductoCreate

router = APIRouter()

# Crear un nuevo producto
@router.post("/", response_model=dict)
async def create_new_producto(producto: ProductoCreate):
    return await create_producto(producto)

# Obtener todos los productos
@router.get("/", response_model=list)
async def list_productos():
    return await get_productos()

# Obtener un producto por ID
@router.get("/{producto_id}", response_model=dict)
async def retrieve_producto(producto_id: str):
    return await get_producto(producto_id)
