import boto3

def search_usuario(event, context):
    body = json.loads(event.get('body', '{}'))  # Esto maneja el caso donde no haya un cuerpo válido
        # Obtener el email y el password
    user_id = body.get('user_id')


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
