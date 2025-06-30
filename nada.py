import boto3
from botocore.exceptions import ClientError, BotoCoreError

b_client = boto3.client("bedrock-agent", region_name="us-east-1")


def list_prompts():
    try:
        res = b_client.list_prompts()
        breakpoint()
    except (BotoCoreError, ClientError) as err:
        print(f"[ERROR] {err}")


def list_range():
    for i in range(1, 3):
        print(f"Number: {i}")


if __name__ == "__main__":
    list_range()
