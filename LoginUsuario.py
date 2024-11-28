import boto3
import hashlib
import uuid
from datetime import datetime, timedelta
import json

# Hashear contraseña
def hash_password(password):
    try:
        # Retorna la contraseña hasheada
        return hashlib.sha256(password.encode()).hexdigest()
    except Exception as e:
        print(f"Error hashing password: {str(e)}")
        raise  # Lanza el error para que sea capturado en el bloque ddddde manejoddddddddddddddd de errores principal

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))  # Esto maneja el caso donde no haya un cuerpo válido
        
        # Obtener el user_id y password
        user_id = body.get('user_id')
        password = body.get('password')

        # Validación de parámetros
        if not user_id or not password:
            raise ValueError("Missing required fields: user_id or password")

        # Hashear la contraseña
        hashed_password = hash_password(password)

        # Conectar a DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('t_usuarios')

        # Obtener el item (usuario) de DynamoDB
        response = table.get_item(Key={'user_id': user_id})

        # Verificar si el usuario existe
        if 'Item' not in response:
            return {
                'statusCode': 403,
                'body': json.dumps({'message': 'Usuario no existe'})
            }

        # Comparar contraseñas
        hashed_password_bd = response['Item']['password']
        if hashed_password == hashed_password_bd:
            # Generar el token
            token = str(uuid.uuid4())
            fecha_hora_exp = datetime.now() + timedelta(minutes=60)
            registro = {
                'token': token,
                'expires': fecha_hora_exp.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Guardar el token en DynamoDB
            tokens_table = dynamodb.Table('t_tokens_acceso')
            tokens_table.put_item(Item=registro)

            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Login exitoso', 'token': token})
            }
        else:
            return {
                'statusCode': 403,
                'body': json.dumps({'message': 'Password incorrecto'})
            }

    except ValueError as ve:
        # Capturar errores de validación (falta de campos)
        print(f"Validation Error: {str(ve)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'message': f"Validation Error: {str(ve)}"})
        }
    
    except boto3.exceptions.S3UploadFailedError as s3_err:
        # Error relacionado con DynamoDB o problemas con la conexión
        print(f"DynamoDB Error: {str(s3_err)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error en la base de datos', 'error': str(s3_err)})
        }
    
    except Exception as e:
        # Capturar cualquier otro error no esperado
        print(f"Exception occurred: {str(e)}")
        print("Detalles del error:", e)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }
