import json
import boto3

client = boto3.client("s3")


def lambda_handler(event, context):
    response = client.get_object(
        Bucket="bucket_name",
        Key="json_file_name.json"
    )

    # Convert from streaming data to dynamodb readable
    json_data = response["Body"].read()
    data = json_data.decode("UTF-8")
    return data
