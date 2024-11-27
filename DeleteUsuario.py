import boto3

def delete_usuario(event, context):
    # Obtener el ID del usuario
    user_id = event['user_id']

    # Conectar con DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_usuarios')

    # Eliminar el ítem
    response = table.delete_item(
        Key={
            'user_id': user_id
        }
    )

    return {
        'statusCode': 200,
        'body': f'Usuario con user_id={user_id} eliminado correctamente.'
    }
