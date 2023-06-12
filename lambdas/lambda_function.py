import boto3


class AccessKey(object):
    def __init__(self, user, region, param_access_key, param_access_secret_key):
        self.user = user
        self.param_region = region
        self.param_access_key = f"/{self.user}/ACCESS_KEY_ID" or param_access_key
        self.param_access_secret_key = f"/{self.user}/ACCESS_SECRET_KEY" or param_access_secret_key

    def create_access_key(self):
        iam = boto3.client("iam")
        access_keys = iam.list_access_keys(UserName=self.user)["AccessKeyMetadata"]


def lambda_handler(event, context):
    pass