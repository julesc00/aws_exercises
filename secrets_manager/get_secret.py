import boto3
from botocore.exceptions import ClientError


def get_secret():
    secret_name = "prod/lulu_app/google_creds"
    region = "us-east-1"
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=region
    )
    try:
        res = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as err:
        print(f"[ERROR] {err}")

    secret = res.get("SecretString")
    return secret


def binary_search(sorted_list, target):
    left = 0
    right = len(sorted_list)
    while left < right:
        mid = (left + right) // 2
        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            left = mid
        else:
            right = mid
    return -1


if __name__ == "__main__":
    test_cases = [
        ([], 5),
        ([1, 2, 3, 4, 5], 3),
        ()
    ]
    print(binary_search())
