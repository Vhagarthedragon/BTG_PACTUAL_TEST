# app/models/sucursal.py
from pydantic import BaseModel

class SucursalCreate(BaseModel):
    nombre: str
    direccion: str
    ciudad: str  # Agrega ciudad
    estado: str  # Agrega estado

class SucursalResponse(BaseModel):
    id: str
    nombre: str
    direccion: str
    ciudad: str
    estado: str
