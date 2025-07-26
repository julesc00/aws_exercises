import json
from http import HTTPStatus

import boto3
from botocore.exceptions import ClientError, BotoCoreError


translate = boto3.client("translate")
api_arn = "arn:aws:execute-api:us-east-1:145622053217:cd2xfzl5m6/*/POST/sf-proxy"

sf_details = {
    "API_AWS_IAM_USER_ARN": "arn:aws:iam::756167685531:user/4h131000-s",
    "API_AWS_EXTERNAL_ID": "MJ40562_SFCRole=5_+QSbSWx7yisbixPCzp6nzCoyl5w=",
}

def lambda_handler(event, context):
    """
    Lambda function to translate text from English to Italian using AWS Translate.
    """
    translated = []
    event_body = event["body"]
    payload = json.loads(event_body)
    rows = payload.get("data", [])
    try:
        for row in rows:
            translated_text = translate.translate_text(
                Text=row[1],
                SourceLanguageCode="en",
                TargetLanguageCode="it"
            )["TranslatedText"]
            translated.append([row[0], translated_text])
        return {
            "statusCode": HTTPStatus.OK,
            "headers": {"Content-Type": "application/json"},
            "data": translated
        }

    except (BotoCoreError, ClientError) as e:
        print(f"[ERROR] Error calling AWS Translate: {e}")
        return {
            "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
            "body": json.dumps({"error": "Failed to translate text."})
        }


if __name__ == "__main__":
    # Example event for local testing
    test_event = {
        "body": json.dumps({
            "data": [
                ["1", "Hello, how are you?"],
                ["2", "This is a test sentence."]
            ]
        })
    }
    print(lambda_handler(test_event, None))