# app/apis/disponibilidad_api.py
from fastapi import APIRouter, HTTPException
from app.services.disponibilidad_service import get_productos_en_sucursal, add_producto_a_sucursal
from app.models.disponibilidad import DisponibilidadCreate

router = APIRouter()

# Obtener los productos disponibles en una sucursal
@router.get("/sucursales/{idSucursal}/productos", response_model=list)
def productos_disponibles_en_sucursal(idSucursal: str):
    productos = get_productos_en_sucursal(idSucursal)  # Remover await aquí
    if not productos:
        raise HTTPException(status_code=404, detail="No se encontraron productos para esta sucursal.")
    return productos

# Agregar un producto a una sucursal
@router.post("/sucursales/productos", response_model=dict)
async def agregar_producto_a_sucursal(disponibilidad: DisponibilidadCreate):
    return await add_producto_a_sucursal(disponibilidad)




