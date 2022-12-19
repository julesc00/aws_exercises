import boto3
from botocore.stub import Stubber
from unittest import TestCase
from unittest.mock import patch
import pytest

import lambdas.index2


class TestLambdaMetadata(TestCase):
    def tests_Metadata_for_lambda_function(self):
        client = boto3.client("lambda")
        stubber = Stubber(client)

        # Expected response from boto3 lambda client's get_function call.
        expected_response = {
            u"Configuration": {"FunctionName": "for-blog", "Runtime": "python3.8"}
        }

        # Stubbed lambda client (with specific parameter) call to get_function results
        # in expected_response.
        stubber.add_response("get_function", expected_response, {"FunctionName": "for-blog"})

        # Patching boto3 attribute of index2.py with stubber
        with patch("index2.boto3") as mock_boto3:
            with stubber:
                mock_boto3.client.return_value = client

                # Call to lambda_handler in index2.py
                lambda_response = lambdas.index2.lambda_handler({}, "context")
                self.assertEqual(lambda_response, expected_response)
