
import base64
import json
import pytest

import boto3
from moto import mock_s3
from botocore.exceptions import ClientError
from lambdas.lambda_function import lambda_handler


test_kinesis_event = {
    "Records": [
        {
            "kinesis": {
                base64.b64encode(json.dumps({
                    "a": "dog",
                    "b": "cat"
                }))
            }
        }
    ]
}

test_s3_event = {
    "Records": [{
        "s3": {
            "bucket": {"name": "test_bucket"},
            "object": {"key": "example/s3/path/key"}
        }
    }]
}

test_sqs_event = {
    "Records": [{
        "body": json.dumps({
            "user_id": "B9B3022F98Fjvjs83AB8/80C185D8",
            "updated_timestamp": "2023-03-03T00:50:47"
        })
    }]
}


@mock_s3
def test_lambda_handler():

    # Set up test bucket
    s3_client = boto3.client("s3", "us-east-1")
    bucket_name = "test_bucket"
    test_data = b'col_1,col_2\n1,2\n3,4\n'

    s3_client.create_bucket(Bucket=bucket_name)
    s3_client.put_object(Body=test_data, Bucket=bucket_name, Key='example/s3/path/key/test_data.csv')

    response = lambda_handler(event=test_s3_event, context={})

    assert response["status"] == "success"

