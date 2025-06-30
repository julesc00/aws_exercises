import boto3
from http import HTTPStatus
from typing import Dict

topic_arn = "arn:aws:sns:us-east-1:145622053217:s3-events-to-lambda-topic"


def send_sns(message: str, subject: str) -> bool:
    sns_client = boto3.client("sns")

    try:
        res = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject
        )
        if res["ResponseMetadata"]["HttpsStatusCode"] == HTTPStatus.OK:
            print(res)
            print("[INFO] Notification sent successfully")
            return True
    except Exception as err:
        print(err)
        return True

def lambda_handler(event: Dict, context: Dict) -> bool:
    print(f"[INFO] Event collected {event}")
    for r in event["Records"]:
        bucket = r["s3"]["bucket"]["name"]
        print(f"[INFO] Bucket name is '{bucket}'")
        r_key = r["s3"]["object"]["key"]
        print(f"[INFO] Record key is {r_key}")

        from_path = f"s3://{bucket}/{r_key}"

        subject = "Process completion notification"
        msg = f"The file is uploaded at: '{from_path}'"
        sns_res = send_sns(message=msg, subject=subject)
        if sns_res:
            print("[INFO] Notification sent")
            return sns_res
        return False


"""
e en https://us05web.zoom.us/j/81019644095?pwd=aLGMQGuIb0aSbmphMJgDorH3m05vop.1 para iniciar o entrar a una reunión de Zoom programada."""