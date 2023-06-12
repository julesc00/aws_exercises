import boto3
from moto import mock_s3
from moto_testing.my_model import MyModel


@mock_s3
def test_my_model_save():
    conn = boto3.resource("s3", region_name="us-east-1")
    # We need to create the bucket since this is all in Moto's "virtual" AWS account
    conn.create_bucket(Bucket="my_bucket")

    my_mode_instance = MyModel("julio", "is awesome")
    my_mode_instance.save()

    body = conn.Object(bucket_name="my_bucket", key="julio").get()[
        "Body"
    ].read().decode("utf-8")

    assert body == "is awesome"
