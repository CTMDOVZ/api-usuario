import boto3
import json

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))  # Esto maneja el caso donde no haya un cuerpo válido
        
        tenant_id = body.get('tenant_id')
        email = body.get('email')
        password = body.get('password')

        if not tenant_id or not email or not password:
            raise ValueError("tenant_id, email, and password are required")

        # Conectar a DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('t_usuarios')

        # Buscar el usuario por email
        response = table.query(
            IndexName='EmailIndex',
            KeyConditionExpression="email = :email",
            ExpressionAttributeValues={':email': email}
        )

        if not response['Items']:
            raise ValueError('Usuario no encontrado')

        user = response['Items'][0]

        if user['password'] != password:
            raise ValueError('Contraseña incorrecta')

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Login exitoso'})
        }

    except Exception as e:
        print(f"Exception: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error', 'details': str(e)})
        }
