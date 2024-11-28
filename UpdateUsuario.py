import boto3

def update_usuario(event, context):
    # Obtener el ID del usuario y los atributos a actualizar
    user_id = event['user_id']
    atributos_actualizar = event['atributos']  # Diccionario con los atributos y valorefdfds a actualizar

    # Conectar con DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_usuarios')

    # Construir la expresión de actualización
    update_expression = "SET " + ", ".join([f"{k} = :{k}" for k in atributos_actualizar.keys()])
    expression_attribute_values = {f":{k}": v for k, v in atributos_actualizar.items()}

    # Actualizar el ítem
    response = table.update_item(
        Key={
            'user_id': user_id
        },
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )

    return {
        'statusCode': 200,
        'body': f'Usuario con user_id={user_id} actualizado correctamente.'
    }
