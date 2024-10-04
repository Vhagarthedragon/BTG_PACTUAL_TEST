import boto3
import uuid
from decimal import Decimal  
from fastapi import HTTPException
from datetime import datetime
from botocore.exceptions import ClientError
from decimal import Decimal 
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
transacciones_table = dynamodb.Table('Transacciones')

# Inicializa la conexión a DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
clientes_table = dynamodb.Table('Clientes')  # Asegúrate de tener la tabla de clientes
transacciones_table = dynamodb.Table('Transacciones')
productos_table = dynamodb.Table('Productos')  # Asegúrate de tener la tabla de productos

async def registrar_transaccion(cliente_id: str, producto_id: str, tipo: str, monto: float):
    # Obtener el cliente para verificar el saldo
    cliente_response = clientes_table.get_item(Key={'id': cliente_id})  # No usar await aquí
    cliente = cliente_response.get('Item')

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # Obtener el producto para verificar el monto mínimo
    producto_response = productos_table.get_item(Key={'id': producto_id})  # No usar await aquí
    producto = producto_response.get('Item')

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Verifica si el monto mínimo del producto es mayor al saldo del cliente
    cliente_saldo_decimal = Decimal(cliente['saldo'])  # Convierte el saldo del cliente a Decimal
    producto_monto_minimo = Decimal(producto['monto_minimo'])  # Convierte el monto mínimo del producto a Decimal


    # Verifica si el cliente tiene saldo suficiente para realizar la transacción
    monto_decimal = Decimal(monto)  # Convertir el monto a Decimal

    if producto_monto_minimo > monto_decimal:
        raise HTTPException(status_code=400, detail=f"El monto mínimo para afiliarse a {producto['nombre']} es de: {producto['monto_minimo']}")

    if cliente_saldo_decimal < monto_decimal:
        raise HTTPException(status_code=400, detail="Saldo insuficiente para realizar la transacción")

    # Actualizar el saldo del cliente
    nuevo_saldo = cliente_saldo_decimal - monto_decimal
    clientes_table.update_item(
        Key={'id': cliente_id},
        UpdateExpression='SET saldo = :val1',
        ExpressionAttributeValues={':val1': str(nuevo_saldo)}  # Convierte a string si es necesario
    )

    # Genera un ID único para la transacción
    transaccion_id = str(uuid.uuid4())  
    fecha_actual = datetime.now().isoformat()  # Genera la fecha actual en formato ISO 8601
    transaccion = {
        'id': transaccion_id,
        'cliente_id': cliente_id,
        'producto_id': producto_id,
        'tipo': tipo,
        'monto': monto_decimal,  # Convierta el monto a Decimal
        'fecha': fecha_actual  # Usa la fecha actual generada
    }
    
    try:
        # Llama a put_item directamente
        transacciones_table.put_item(Item=transaccion)
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Error al registrar transacción: {e.response['Error']['Message']}")

    return transaccion  # Devuelve la transacción para confirmación

async def cancelar_transaccion_servicio(transaccion_id: str, cliente_id: str):
    # Obtener la transacción para asegurarnos de que existe
    try:

        transaccion_response = transacciones_table.get_item(Key={
            'id': transaccion_id       # Clave de clasificación
        })


        transaccion = transaccion_response.get('Item')
        
        if not transaccion:
            raise HTTPException(status_code=404, detail="Transacción no encontrada")

        # Obtener el cliente para actualizar su saldo
        cliente_response = clientes_table.get_item(Key={'id': cliente_id})
        cliente = cliente_response.get('Item')
        
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        # Actualizar el saldo del cliente sumando el monto de la transacción cancelada
        monto_transaccion = Decimal(transaccion['monto'])  # Convertir monto a Decimal
        nuevo_saldo = Decimal(cliente['saldo']) + monto_transaccion
        
        # Actualizar la transacción para marcarla como "afiliacion cancelada"
        transacciones_table.update_item(
            Key={
               
                'id': transaccion_id       # Clave de clasificación
            },
            UpdateExpression='SET #tipo = :tipo',
            ExpressionAttributeNames={'#tipo': 'tipo'},
            ExpressionAttributeValues={':tipo': 'afiliacion cancelada'}
        )

        # Actualizar el saldo del cliente en la tabla de Clientes
        clientes_table.update_item(
            Key={'id': cliente_id},
            UpdateExpression='SET saldo = :nuevo_saldo',
            ExpressionAttributeValues={':nuevo_saldo': str(nuevo_saldo)}  # Convertir a string si es necesario
        )

        return {"message": "Transacción cancelada y saldo del cliente actualizado"}

    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Error al cancelar transacción: {e.response['Error']['Message']}")


async def get_transacciones(cliente_id: str):
    try:
        response = transacciones_table.scan(
        FilterExpression=Attr('cliente_id').eq(cliente_id)
        )
        return response.get('Items', [])
    except ClientError as e:
        raise HTTPException(status_code=500, detail="Error al obtener transacciones: " + e.response['Error']['Message'])
