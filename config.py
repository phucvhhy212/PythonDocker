
import boto3
from botocore.exceptions import ClientError
import json


def get_secret():

    secret_name = "my-flask-secret"
    region_name = "ap-southeast-1"
    

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        aws_access_key_id='AKIA5GO2RRGUTDP34HQU',
        aws_secret_access_key='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'
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
            
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    # Your code goes here.
    return json.loads(secret)


class Config:
    secrets =  get_secret()
    FLASK_APP = "main.py"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{secrets['username']}:{secrets['password']}@{secrets['host']}:{secrets['port']}/{secrets['database']}"


class DevConfig(Config):
    FLASK_ENV = "development"
    FLASK_DEBUG = True