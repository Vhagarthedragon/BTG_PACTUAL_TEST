from pydantic import BaseModel
from datetime import datetime

class TransaccionCreate(BaseModel):
    cliente_id: str
    producto_id: str
    monto: float
    tipo: str
    fecha: datetime = None  # Puede ser opcional

class TransaccionResponse(BaseModel):
    id: str
    cliente_id: str
    producto_id: str
    monto: int
    tipo: str
    fecha: datetime
