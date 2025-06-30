from typing import Dict
import boto3
from botocore.exceptions import ClientError


ACCOUNTS = {
    "my_aws_acc": "145622053217",
    "other_acc": "123456789012"
}


def check_aws_acc_id(accounts: Dict[str, int]) -> str:
    try:
        sts = boto3.client("sts")
        res = sts.get_caller_identity()
        acc = res.get("Account")
        for k, v in accounts.items():
            if acc == v:
                return k
        return f"[INFO] '{acc}' is not registered in the specified aws accounts object, please update it."
    except ClientError as err:
        print(f"[ERROR] {err}")


if __name__ == "__main__":
    print(check_aws_acc_id(ACCOUNTS))