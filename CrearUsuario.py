import boto3
import hashlib
import json

# Hashear contraseña
def hash_password(password):
    # Retorna la contraseña hasheada
    try:
        return hashlib.sha256(password.encode()).hexdigest()
    except Exception as e:
        print(f"Error hashing password: {str(e)}")
        raise

# Función que maneja el registro de user y validación del password
def lambda_handler(event, context):
    try:
        # Obtener el email y el password
        user_id = event.get('user_id')
        password = event.get('password')

        # Verificar que el user_id y el password existen
        if not user_id or not password:
            raise ValueError("Invalid request body: missing user_id or password")

        # Hashear la contraseña antes de almacenarla
        hashed_password = hash_password(password)

        # Conectar DynamoDB
        dynamodb = boto3.resource('dynamodb')
        t_usuarios = dynamodb.Table('t_usuarios')

        # Almacenar los datos del user en la tabla de usuarios en DynamoDB
        t_usuarios.put_item(
            Item={
                'user_id': user_id,
                'password': hashed_password,
            }
        )

        # Retornar un código de estado HTTP 200 (OK) y un mensaje de éxito
        mensaje = {
            'message': 'User registered successfully',
            'user_id': user_id
        }
        return {
            'statusCode': 200,
            'body': json.dumps(mensaje)
        }

    except ValueError as ve:
        # Captura de errores de validación (por ejemplo, falta el user_id o password)
        print(f"Validation Error: {str(ve)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(ve)})
        }

    except boto3.exceptions.S3UploadFailedError as s3_err:
        # Error relacionado con S3 o DynamoDB
        print(f"S3 Upload Error: {str(s3_err)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to upload to DynamoDB', 'details': str(s3_err)})
        }

    except Exception as e:
        # Captura de cualquier otra excepción
        print(f"Exception occurred: {str(e)}")
        print("Detailed error:", e, "Stack Trace:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error', 'details': str(e)})
        }
