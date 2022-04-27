import jwt
import boto3
from datetime import datetime, timedelta
import os
import base64
import json

SECRET_PRIVATE_KEY = os.getenv('SECRET_PRIVATE_KEY')
IVS_CHANNEL_ARN = os.getenv("IVS_CHANNEL_ARN")


def get_private_key(secret_id):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(
        SecretId=secret_id,
    )
    if not response:
        return None
    if "SecretString" not in response:
        return None
    else:
        return response['SecretString']


def sign_request(private_key, channel_arn):
    payload = {
        "aws:channel-arn": channel_arn,
        "aws:access-control-allow-origin": "*",
        "exp": datetime.now() + timedelta(days=3)}
    encoded = jwt.encode(payload, private_key, algorithm="ES384")
    return encoded


def handler(event, context):
    private_key_base64 = get_private_key(SECRET_PRIVATE_KEY)
    private_key = base64.b64decode(private_key_base64)
    token = sign_request(private_key, IVS_CHANNEL_ARN)
    response = {'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,GET'
                },
                'body': json.dumps({'token': token})}
    return response
