import boto3
import json

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))  # Captura el cuerpo del evento
        email = body.get('email')

        if not email:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Email is required'})
            }

        # Conectar DynamoDB
        dynamodb = boto3.resource('dynamodb')
        t_usuarios = dynamodb.Table('t_usuarios')

        # Realizar la consulta utilizando el GSI por email
        response = t_usuarios.query(
            IndexName="EmailIndex",
            KeyConditionExpression=boto3.dynamodb.conditions.Key('email').eq(email)
        )

        # Retornar los usuarios encontrados
        return {
            'statusCode': 200,
            'body': json.dumps({'users': response['Items']})
        }

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error', 'details': str(e)})
        }
