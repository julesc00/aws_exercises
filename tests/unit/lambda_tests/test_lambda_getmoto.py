"""
Source: https://github.com/getmoto/moto/blob/96e5b1993d7f2451443bfabff4265029ac6625af/tests/test_awslambda/test_lambda.py
"""
from __future__ import unicode_literals

import base64
import uuid
import io
import json
import time
import zipfile

import boto3
import botocore.client
from botocore.exceptions import ClientError
from moto import (
    mock_dynamodb,
    mock_lambda,
    mock_s3,
    mock_ec2,
    mock_sns,
    mock_logs,
    settings,
    mock_sqs
)

# from nose.tools import assert_raises

_lambda_region = "us-east-1"
boto3.setup_default_session(region_name=_lambda_region)


def _process_lambda(func_str):
    zip_output = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_output, "w", zipfile.ZIP_DEFLATED)
    zip_file.writestr("lambda_function.py", func_str)
    zip_file.close()
    zip_output.seek(0)

    return zip_output.read()


def get_test_zip_file():
    p_func = """
def lambda_handler(event, context):
    return event
    """
    return _process_lambda(p_func)


def get_test_zip_file2():
    func_str = """
import boto3

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2', region_name='us-east-1', endpoint_url='http://{base_url}')

    volume_id = event.get('volume_id')
    vol = ec2.Volume(volume_id)

    print('get volume details for %s\\nVolume - %s  state=%s, size=%s' % (volume_id, volume_id, vol.state, vol.size))
    return event
""".format(
        base_url="motoserver:5000"
        if settings.TEST_SERVER_MODE
        else "ec2.us-west-2.amazonaws.com"
    )
    return _process_lambda(func_str)


def get_test_zip_file3():
    p_func = """
def lambda_handler(event, context):
    print("get_test_zip_file3 success")
    return event
"""
    return _process_lambda(p_func)


def get_test_zip_file4():
    p_func = """
def lambda_handler(event, context):    
    raise Exception('I failed!')
"""
    return _process_lambda(p_func)


@mock_lambda
def test_invoke_request_response_function():
    conn = boto3.client("lambda", "us-east-1")
    conn.create_function(
        FunctionName="testFunction",
        Runtime="python3.8",
        Role="test-iam-role",
        Handler="lambda_function.lambda_handler",
        Code={"ZipFile": get_test_zip_file()},
        Description="test lambda function",
        Timeout=3,
        MemorySize=128,
        Publish=True
    )

    in_data = {"msg": "So long and thanks for all the fish"}
    success_result = conn.invoke(
        FunctionName="testFunction",
        InvocationType="RequestResponse",
        Payload=json.dumps(in_data)
    )

    success_result["StatusCode"].should.equal(202)
    result_obj = json.loads(
        base64.b64decode(success_result["LogResult"]).decode("utf-8")
    )
