# app/services/sucursal_service.py
import boto3
import uuid
from botocore.exceptions import ClientError
from fastapi import HTTPException
from app.models.sucursal import SucursalCreate  # Asegúrate de que este modelo tenga las propiedades correctas

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
sucursales_table = dynamodb.Table('Sucursales')

# Crear una nueva sucursal
async def create_sucursal(sucursal_data: SucursalCreate):
    sucursal_id = str(uuid.uuid4())  # Genera un ID único para la sucursal
    try:
        sucursales_table.put_item(
            Item={
                'id': sucursal_id,
                'nombre': sucursal_data.nombre,
                'direccion': sucursal_data.direccion,
                'ciudad': sucursal_data.ciudad,  # Asegúrate de que 'ciudad' esté en el modelo
                'estado': sucursal_data.estado  # Asegúrate de que 'estado' esté en el modelo
            }
        )
        return {"message": "Sucursal creada con éxito", "id": sucursal_id}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Error al crear sucursal: {e.response['Error']['Message']}")

# Obtener todas las sucursales
async def get_sucursales():
    try:
        response = sucursales_table.scan()  # Usa scan para obtener todas las sucursales
        return response.get('Items', [])
    except ClientError as e:
        raise HTTPException(status_code=500, detail="Error al obtener sucursales")

# Obtener una sucursal por ID
async def get_sucursal(sucursal_id: str):
    try:
        response = sucursales_table.get_item(Key={'id': sucursal_id})
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail="Sucursal no encontrada")
        return response['Item']
    except ClientError as e:
        raise HTTPException(status_code=500, detail="Error al obtener sucursal")

# Eliminar una sucursal por ID
async def delete_sucursal(sucursal_id: str):
    try:
        response = sucursales_table.delete_item(
            Key={'id': sucursal_id},
            ReturnValues='ALL_OLD'  # Devuelve la sucursal eliminada si existía
        )
        if 'Attributes' not in response:
            raise HTTPException(status_code=404, detail="Sucursal no encontrada")
        return {"message": "Sucursal eliminada con éxito"}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar sucursal: {e.response['Error']['Message']}")
