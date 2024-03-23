import json


def lambda_handler(event, context):
    print(event)
    content = "<p>Hello, World from my lambda using ALB!</p>"
    return {
        "statusCode": 200,
        "statusDescription": "200 OK",
        "isBase64Encoded": False,
        "body": json.dumps(content),
        "headers": {
            "Content-Type": "text/html",
        },
    }
