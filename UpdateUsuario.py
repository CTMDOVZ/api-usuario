import boto3
import json

def lambda_handler(event, context):
    try:
        tenant_id = event['pathParameters']['tenant_id']
        user_id = event['pathParameters']['user_id']
        body = json.loads(event.get('body', '{}'))

        # Conectar a DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('t_usuarios')

        # Actualizar los atributos del usuario
        table.update_item(
            Key={
                'tenant_id': tenant_id,
                'user_id': user_id
            },
            UpdateExpression="set email = :email, password = :password",
            ExpressionAttributeValues={
                ':email': body['email'],
                ':password': body['password']
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Usuario actualizado con éxito'})
        }

    except Exception as e:
        print(f"Exception: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error', 'details': str(e)})
        }
