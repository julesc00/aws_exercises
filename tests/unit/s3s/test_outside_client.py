import boto3
from moto import mock_s3


outside_client = boto3.client("s3")
s3 = boto3.resource("s3")


@mock_s3
def test_mock_works_with_client_or_resource_created_outside():
    from moto.core import (patch_client, patch_resource)

    patch_client(outside_client)
    patch_resource(s3)

    assert outside_client.list_buckets()["Buckets"] == []
    assert list(s3.buckets.all()) == []


"""
For Tox, Travis CI, Github Actions, and other build systems, you might need to also create fake AWS credentials. 
The following command will create the required file with some bogus-credentials:

mkdir ~/.aws && touch ~/.aws/credentials && echo -e "[default]\naws_access_key_id = test\naws_secret_access_key = test" > ~/.aws/credentials
"""