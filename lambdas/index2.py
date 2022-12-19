import boto3


"""
Unit testing AWS Lambda interacting with other AWS Services/APIs
"""


def lambda_handler(event, context):
    lambda_client = boto3.client("lambda")
    response = lambda_client.get_function(
        FunctionName="for-blog"
    )
    return response
