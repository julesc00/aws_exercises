import unittest
import pytest
import boto3
import botocore

from lambdas.lambda_function import AccessKey
from moto import mock_iam, mock_ssm


class AccessKeyTestCase(unittest.TestCase):

    def test_init(self):
        username = "abc"
        a = AccessKey(username, "us-east-1")

        assert a.user == username
        assert a.param_region == "us-east-1"
        assert a.param_access_key == f"/{username}/ACCESS_KEY_ID"
        assert a.param_access_secret_key == f"/{username}/ACCESS_SECRET_KEY"

    def test_custom_params(self):
        a = AccessKey("abc", "us-east-1", "/custom/access", "/custom/secret")

        assert a.param_access_key == "/custom/access"
        assert a.param_access_secret_key == "/custom/secret"

    @mock_iam
    @mock_ssm
    def test_setting_parameters(self):
        user, region = "abc", "us-east-1"
        custom_access, custom_secret = "/custom/access", "/custom/secret"
        iam = boto3.client("iam")
        iam.create_user(UserName=user)

        a = AccessKey(user, region, custom_access, custom_secret)
        a.create_access_key()

        ssm = boto3.client("ssm", region_name=region)
        key = ssm.get_parameter(Name=custom_access)["Parameter"]["Value"]
        secret = ssm.get_parameter(Name=custom_secret)["Parameter"]["Value"]

        assert key is not None
        assert secret is not None


if __name__ == "__main__":
    unittest.main()
