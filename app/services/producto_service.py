# app/services/producto_service.py
import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException
from app.models.productos import ProductoCreate

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
productos_table = dynamodb.Table('Productos')

# Crear un nuevo producto
async def create_producto(producto_data: ProductoCreate):
    try:
        productos_table.put_item(
            Item={
                'id': producto_data.id,
                'nombre': producto_data.nombre,
                'monto_minimo': producto_data.monto_minimo,
                'categoria': producto_data.categoria
            }
        )
        return {"message": "Producto creado con éxito", "id": producto_data.id}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Error al crear producto: {e.response['Error']['Message']}")

# Obtener todos los productos
async def get_productos():
    try:
        response = productos_table.scan()
        return response.get('Items', [])
    except ClientError as e:
        raise HTTPException(status_code=500, detail="Error al obtener productos")

# Obtener un producto por ID
async def get_producto(producto_id: str):
    try:
        response = productos_table.get_item(Key={'id': producto_id})
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return response['Item']
    except ClientError as e:
        raise HTTPException(status_code=500, detail="Error al obtener producto")
