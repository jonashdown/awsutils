import boto3
import os

access_key_id = os.getenv('AWS_ACCESS_KEY_ID_SOURCE')
secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY_SOURCE')
aws_session_token = os.getenv('AWS_SESSION_TOKEN_SOURCE')


access_key_id_target = os.getenv('AWS_ACCESS_KEY_ID_TARGET')
secret_access_key_target = os.getenv('AWS_SECRET_ACCESS_KEY_TARGET')
aws_session_token_target = os.getenv('AWS_SESSION_TOKEN_TARGET')

dynamoclient = boto3.client('dynamodb',
    region_name='eu-west-1',
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
    aws_session_token=aws_session_token)

dynamotargetclient = boto3.client(
    'dynamodb',
    region_name='eu-west-1',
    aws_access_key_id=access_key_id_target,
    aws_secret_access_key=secret_access_key_target,
    aws_session_token=aws_session_token_target)

dynamopaginator = dynamoclient.get_paginator('scan')
tabname='node-graph'
targettabname='node-graph'
dynamoresponse = dynamopaginator.paginate(
    TableName=tabname,
    Select='ALL_ATTRIBUTES',
    ReturnConsumedCapacity='NONE',
    ConsistentRead=True
)
for page in dynamoresponse:
    for item in page['Items']:
        dynamotargetclient.put_item(
            TableName=targettabname,
            Item=item
        )
