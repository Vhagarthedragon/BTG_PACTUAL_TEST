from pydantic import BaseModel

class ClienteCreate(BaseModel):
    id: str = None
    nombre: str
    apellidos: str
    ciudad: str
    email: str = None
    saldo: int = 500000

class ClienteResponse(ClienteCreate):
    id: str

class SaldoUpdate(BaseModel):
    nuevo_saldo: int  # Define el campo nuevo_saldo como un entero