# app/services/cliente_service.py
import boto3
import uuid
from botocore.exceptions import ClientError
from fastapi import HTTPException
from app.models.cliente import ClienteResponse

from dotenv import load_dotenv
import os

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

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
clientes_table = dynamodb.Table('Clientes')

async def create_cliente(cliente_data):
    cliente_id = str(uuid.uuid4())
    cliente_data.id = cliente_id
    try:
        clientes_table.put_item(Item=cliente_data.dict())
        return {"message": "Cliente creado con éxito", "id": cliente_id}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Error al crear cliente: {e.response['Error']['Message']}")

async def get_clientes():
    try:
        response = clientes_table.scan()
        return response.get('Items', [])
    except ClientError as e:
        raise HTTPException(status_code=500, detail="Error al obtener clientes")

async def get_cliente(cliente_id: str):
    try:
        response = clientes_table.get_item(Key={'id': cliente_id})
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return response['Item']
    except ClientError as e:
        raise HTTPException(status_code=500, detail="Error al obtener cliente")

async def delete_cliente(cliente_id: str):
    try:
        response = clientes_table.delete_item(Key={'id': cliente_id}, ReturnValues='ALL_OLD')
        if 'Attributes' in response:
            return {"message": "Cliente eliminado con éxito"}
        else:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
    except ClientError as e:
        raise HTTPException(status_code=500, detail="Error al eliminar cliente")

# Agregar la función para actualizar el saldo
async def update_cliente_saldo(cliente_id: str, nuevo_saldo: int):
    try:
        response = clientes_table.update_item(
            Key={'id': cliente_id},
            UpdateExpression="set saldo=:s",
            ExpressionAttributeValues={':s': nuevo_saldo},
            ReturnValues="UPDATED_NEW"  # Opcional: devuelve el nuevo saldo actualizado
        )
        return response  # Retorna la respuesta, opcionalmente
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar saldo: {e.response['Error']['Message']}")

        

# Nueva función para consultar el saldo
async def get_cliente_saldo(cliente_id: str):
    try:
        response = clientes_table.get_item(Key={'id': cliente_id})
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return response['Item'].get('saldo')  # Devuelve el saldo o 0 si no está definido
    except ClientError as e:
        raise HTTPException(status_code=500, detail="Error al obtener saldo del cliente: " + e.response['Error']['Message'])