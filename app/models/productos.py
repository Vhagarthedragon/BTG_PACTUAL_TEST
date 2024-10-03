# app/models/productos.py
from pydantic import BaseModel

class ProductoCreate(BaseModel):
    id: str
    nombre: str
    monto_minimo: int
    categoria: str

class ProductoResponse(ProductoCreate):
    pass
