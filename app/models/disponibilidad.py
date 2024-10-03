# app/models/disponibilidad.py
from pydantic import BaseModel

class DisponibilidadCreate(BaseModel):
    idSucursal: str
    idProducto: str

class DisponibilidadResponse(DisponibilidadCreate):
    pass
