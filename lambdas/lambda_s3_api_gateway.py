import json
import boto3
from botocore import exceptions
from logging import error as logging_error

s3_client = boto3.client("s3")


def lambda_handler(event: dict, context: dict):
    data = get_s3_object(s3_client, event.get("bucket_name"), event.get("key_name"))
    return {
        "statusCode": 200,
        "body": covert_bytes_to_string(data)
    }


def get_s3_object(aws_client, bucket: str, key: str):
    try:
        client = aws_client.client("s3")
        response = client.get_object(
            Bucket=bucket,
            Key=key
        )
        return response
    except exceptions.DataNotFoundError as client_error:
        logging_error({
            "message": "Some error",
            "body": client_error
        })
        pass
    return exceptions.ConnectionError


def covert_bytes_to_string(body):
    data_bytes = body.get("Body").read()
    data_strings = data_bytes.decode("UTF-8")
    return {
        "statusCode": 200,
        "body": json.loads(data_strings)
    }

