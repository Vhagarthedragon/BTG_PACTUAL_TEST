# app/services/disponibilidad_service.py
import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException
from boto3.dynamodb.conditions import Key  # Asegúrate de que esta línea esté incluida

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
disponibilidad_table = dynamodb.Table('Disponibilidad')
productos_table = dynamodb.Table('Productos')

from app.models.disponibilidad import DisponibilidadCreate

# Agregar un producto a una sucursal
async def add_producto_a_sucursal(disponibilidad_data: DisponibilidadCreate):
    try:
        disponibilidad_table.put_item(
            Item={
                'idSucursal': disponibilidad_data.idSucursal,
                'idProducto': disponibilidad_data.idProducto
            }
        )
        return {"message": "Producto agregado a la sucursal con éxito"}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Error al agregar producto: {e.response['Error']['Message']}")

def get_productos_en_sucursal(idSucursal: str):
    try:
        # Consulta la tabla 'Disponibilidad' para obtener los productos de la sucursal
        disponibilidad_items = disponibilidad_table.query(
            KeyConditionExpression=Key('idSucursal').eq(idSucursal)
        )

        productos_disponibles = []
        for item in disponibilidad_items.get('Items', []):
            id_producto = item['idProducto']

            # Obtener detalles del producto usando su ID
            producto_details = get_producto_por_id(id_producto)  # Cambiar a función sin await
            if producto_details:
                productos_disponibles.append({
                    "id": producto_details["id"],
                    "nombre": producto_details["nombre"],
                })

        return productos_disponibles

    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener productos: {e.response['Error']['Message']}")

def get_producto_por_id(producto_id: str):
    try:
        response = productos_table.get_item(Key={'id': producto_id})
        return response.get('Item', None)  # Devuelve el producto si existe
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el producto: {e.response['Error']['Message']}")
