import json
import os
import logging

import boto3

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
DB_TABLE_NAME = os.environ.get("DB_TABLE_NAME", "julio-test")

S3_CLIENT = boto3.client("s3")
DB_CLIENT = boto3.resource("dynamodb", region_name=AWS_REGION)
DB_TABLE = DB_CLIENT.Table(DB_TABLE_NAME)


def get_data_from_file(bucket, key):
    """
    Function reads json file uploaded to s3 bucket
    :param bucket: bucket name
    :param key: object key
    :return: {"statusCode": 200, "message": "SUCCESS"}
    """
    response = S3_CLIENT.get_object(
        Bucket=bucket,
        Key=key
    )
    content = response["Body"]
    data = json.loads(content.read())
    LOGGER.info(f"{bucket}/{key} file content: {data}")
    return data


def save_data_to_db(data):
    """
    Function saves data to DynamoDB table.
    :param data:
    :return: json
    """
    result = DB_TABLE.put_item(Item=data)
    return result


def handler(event, context):
    LOGGER.info(f"Event structure: {event}")
    for record in event["Records"]:
        s3_bucket = record["s3"]["bucket"]["name"]
        s3_file = record["s3"]["object"]["key"]
        data = get_data_from_file(s3_bucket, s3_file)
        for item in data:
            save_data_to_db(item)
        return {
            "statusCode": 200,
            "message": "SUCCESS"
        }
