import base64

import requests
import boto3
import pytest
from moto import mock_kms


"""
Source: https://www.learnaws.org/2021/02/21/test-aws-kms-boto/
"""

@mock_kms
def test_list_keys():
    conn = boto3.client("kms", "us-east-1")
    key = conn.create_key(Description="my key")

    response = conn.list_keys()
    assert len(response.get("Keys")) == 1


@mock_kms
def test_describe_key():
    """
    Sample key content

     {'KeyMetadata':
        {
            'AWSAccountId': '123456789012'
            'Arn': 'arn:aws:kms:us-east-1:123456789012:key/32299142-113e-47f1-bf55-3a32400a4654',
            'CreationDate': datetime.datetime(2023, 5, 26, 9, 4, 29, 147500, tzinfo=tzlocal()),
            'CustomerMasterKeySpec': 'SYMMETRIC_DEFAULT', ...},
            'ResponseMetadata': {
                'HTTPHeaders': {'server': 'amazon.com'},
                'HTTPStatusCode': 200, 'RetryAttempts': 0
            }
        }

        KeyId sample: 50e70ec0-35d2-4362-91cd-091c12a26abd
    """
    conn = boto3.client("kms", "us-east-1")
    key = conn.create_key(Description="my key")
    key_id = key.get("KeyMetadata").get("KeyId")

    key = conn.describe_key(KeyId=key_id)
    assert key["KeyMetadata"]["Description"] == "my key"


@mock_kms
def test_generated_data_key():
    conn = boto3.client("kms", "us-east-1")
    key = conn.create_key(Description="my key")
    key_id = key["KeyMetadata"]["KeyId"]

    data_key = conn.generate_data_key(KeyId=key_id, NumberOfBytes=32)
    # Plaintext must NOT be base64-encoded
    with pytest.raises(Exception):
        base64.b64decode(data_key["Plaintext"], validate=True)


@mock_kms
def test_decrypt_data_key():
    conn = boto3.client("kms", "us-east-1")
    key = conn.create_key(Description="my key")
    key_id = key["KeyMetadata"]["KeyId"]

    data_key = conn.generate_data_key(
        KeyId=key_id,
        NumberOfBytes=32
    )

    encrypted_data_key, plaintext_data_key = data_key["CiphertextBlob"], data_key["Plaintext"]
    response = conn.decrypt(CiphertextBlob=encrypted_data_key)

    assert response["Plaintext"] == plaintext_data_key


def test_requests():
    post_data = requests.post()
