import boto3
import hashlib
import json

def hash_password(password):
    try:
        return hashlib.sha256(password.encode()).hexdigest()
    except Exception as e:
        print(f"Error hashing password: {str(e)}")
        raise

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))  # Esto maneja el caso donde no haya un cuerpo válido
        
        # Obtener los parámetros requeridos
        tenant_id = body.get('tenant_id')
        user_id = body.get('user_id')
        email = body.get('email')
        password = body.get('password')
        created_at = body.get('created_at', '2024-11-27T00:00:00Z')  # Fecha de creación por defecto

        # Verificar que los parámetros esenciales están presentes
        if not tenant_id or not user_id or not email or not password:
            raise ValueError("tenant_id, user_id, email, and password are required")

        # Hashear la contraseña
        hashed_password = hash_password(password)

        # Conectar a DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('t_usuarios')

        # Crear el ítem del usuario
        item = {
            'tenant_id': tenant_id,
            'user_id': user_id,
            'email': email,
            'password': hashed_password,
            'created_at': created_at
        }

        # Almacenar el ítem en DynamoDB
        table.put_item(Item=item)

        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'Usuario creado con éxito', 'usuario': item})
        }

    except ValueError as ve:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(ve)})
        }

    except Exception as e:
        print(f"Exception: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error', 'details': str(e)})
        }
