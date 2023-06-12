
import boto3


class MyModel:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def save(self):
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.put_object(
            Bucket="my_bucket",
            Key=self.name,
            Body=self.value
        )
