import boto3

def search_usuario(event, context):
    # Obtener el ID del usuario
    user_id = event['user_id']

    # Conectar con DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_usuarios')

    # Buscar el ítem
    response = table.get_item(
        Key={
            'user_id': user_id
        }
    )

    # Verificar si el ítem fue encontrado
    if 'Item' in response:
        return {
            'statusCode': 200,
            'body': response['Item']
        }
    else:
        return {
            'statusCode': 404,
            'body': f'Usuario con user_id={user_id} no encontrado.'
        }
