import os
import json
import boto3
from botocore.exceptions import ClientError
import logging

client = boto3.client("s3")

test_data = {
    "name": "aws-made-easy"
}


def write_obj_to_s3(data: dict):
    # If data from file.
    obj_name = os.path.basename("file_name")
    json_data = json.dumps(data).encode("UTF-8")
    try:
        # Write object to bucket
        response = client.put_object(
            Body=json_data if obj_name is None else obj_name,
            Bucket="bucket_name",
            Key="test_data.json"
        )
        return response
    except ClientError as e:
        logging.error(e)
        pass


if __name__ == "__main__":
    write_obj_to_s3(test_data)
