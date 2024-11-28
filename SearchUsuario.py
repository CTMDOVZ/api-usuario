import boto3
import json

def lambda_handler(event, context):
    try:
        tenant_id = event['pathParameters']['tenant_id']

        # Conectar a DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('t_usuarios')

        # Obtener todos los usuarios del tenant
        response = table.query(
            KeyConditionExpression="tenant_id = :tenant_id",
            ExpressionAttributeValues={':tenant_id': tenant_id}
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'usuarios': response['Items']})
        }

    except Exception as e:
        print(f"Exception: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error', 'details': str(e)})
        }
