import boto3

def delete_usuario(event, context):
    body = json.loads(event.get('body', '{}'))  # Esto maneja el caso donde no haya un cuerpo válido
        # Obtener el email y el password
    user_id = body.get('user_id')


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
