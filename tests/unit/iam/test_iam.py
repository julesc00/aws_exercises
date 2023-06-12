import os

import boto3
import botocore.exceptions
from moto import mock_ec2
from moto.core import set_initial_no_auth_action_count

"""
Moto also has the ability to authenticate and authorize actions, just like it’s done by IAM in AWS.
This functionality can be enabled by either setting the INITIAL_NO_AUTH_ACTION_COUNT environment
variable or using the set_initial_no_auth_action_count decorator. Note that the current implementation
is very basic, see the source code for more information.

INITIAL_NO_AUTH_ACTION_COUNT
If this environment variable is set, moto will skip performing any authentication as many times as the
variable’s value, and only starts authenticating requests afterwards. If it is not set, it defaults to
infinity, thus moto will never perform any authentication at all.

set_initial_no_auth_action_count
This is a decorator that works similarly to the environment variable, but the settings are only valid in the
function’s scope. When the function returns, everything is restored.
"""


@set_initial_no_auth_action_count(4)
@mock_ec2
def test_describe_instances_allowed():
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "ec2:Describe*",
                "Resource": "*"
            }
        ]
    }

    access_key = {
        "AccessKeyId": os.environ.get("AWS_ACCESS_KEY"),
        "SecretAccessKey": os.environ.get("AWS_SECRET_ACCESS_KEY")
    }
    # create access key for an IAM user/assumed role that has the policy above.
    # this part should call __exactly__ 4 AWS actions, so that authentication and authorization starts
    # exactly after this
    try:
        ec2_client = boto3.client(
            "ec2",
            region_name="us-east-1",
            aws_access_key_id="AKIASDZ6AGFQTGB25X7D",
            aws_secret_access_key="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"
        )
        instances = ec2_client.describe_instances()["Reservations"][0]["Instances"]
        print(instances)
        assert len(instances) == 0
    except botocore.exceptions.ClientError as error:
        print(f"Some error occurred: {error}")
