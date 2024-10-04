# app/main.py
from fastapi import FastAPI
import os
from dotenv import load_dotenv
import boto3
from fastapi.middleware.cors import CORSMiddleware
from app.apis import cliente_api, transaccion_api, sucursal_api, disponibilidad_api, producto_api

app = FastAPI()

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las credenciales de las variables de entorno
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Crear una sesión de boto3
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto según tu entorno
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Incluir las rutas de las diferentes APIs
app.include_router(cliente_api.router, prefix="/clientes", tags=["Clientes"])
app.include_router(transaccion_api.router, prefix="/transacciones", tags=["Transacciones"])
app.include_router(sucursal_api.router, prefix="/sucursales", tags=["Sucursales"])
app.include_router(disponibilidad_api.router, prefix="/disponibilidad", tags=["Disponibilidad"])
app.include_router(producto_api.router, prefix="/productos", tags=["Productos"])


@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Gestión de Sucursales y Productos"}


