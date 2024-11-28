import boto3
import hashlib
import json
import datetime

# Hashear contraseña
def hash_password(password):
    try:
        return hashlib.sha256(password.encode()).hexdigest()
    except Exception as e:
        print(f"Error hashing password: {str(e)}")
        raise

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))  # Esto maneja el caso donde no haya un cuerpo válido
        
        # Obtener los datos del usuario
        id_aerolinea = body.get('id_aerolinea')
        user_id = body.get('user_id')
        email = body.get('email')
        password = body.get('password')

        if not user_id or not email or not password:
            raise ValueError("Invalid request body: missing user_id, email or password")

        # Hashear la contraseña antes de almacenarla
        hashed_password = hash_password(password)

        # Conectar DynamoDB
        dynamodb = boto3.resource('dynamodb')
        t_usuarios = dynamodb.Table('t_usuarios')

        # Almacenar el usuario en DynamoDB
        t_usuarios.put_item(
            Item={
                'id_aerolinea':id_aerolinea,
                'user_id': user_id,
                'email': email,
                'password': hashed_password,
                'created_at': str(datetime.datetime.now())  # Fecha de creación
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User registered successfully'})
        }

    except ValueError as ve:
        print(f"Validation Error: {str(ve)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(ve)})
        }

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error', 'details': str(e)})
        }
