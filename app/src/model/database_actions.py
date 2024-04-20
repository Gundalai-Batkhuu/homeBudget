# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/
import json

import boto3
import psycopg2
from botocore.exceptions import ClientError


def get_secret(secret_name, region_name):

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']

    return secret

if __name__ == "__main__":
    secret_name = "rds!db-719c2fd1-423b-4e63-b785-7b616f975982"
    region_name = "ap-southeast-2"
    secret = get_secret(secret_name, region_name)

    secret_dict = json.loads(secret)

    username = secret_dict['username']
    passw = secret_dict['password']
    print(username)
    print(passw)

    try:
        conn = psycopg2.connect(host="terraform-20240419111553068200000001.cdf47oegxmwl.ap-southeast-2.rds.amazonaws.com",
                                port='5432',
                                database="homeBudget",
                                user=username,
                                password=passw)
        print("Connected to database")
    except psycopg2.DatabaseError as e:
        print("Error connecting to database")
        print(e)

    conn.close()
    print("Connection closed")
