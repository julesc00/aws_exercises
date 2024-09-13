import datetime
import json

import boto3

eventbridge = boto3.client('events')


def lambda_handler(event, context):
    """
    Lambda handler function to publish events to Amazon EventBridge.
    """
    # Publish event to EventBridge
    response = eventbridge.put_events(
        Entries=[
            {
                'Source': 'Lambda publish',
                "Time": datetime.time(),
                'DetailType': 'Custom Event Demo',
                'Detail': json.dumps(event),
                'EventBusName': 'default'
            }
        ]
    )

    return {
        'statusCode': 200,
        'body': response
    }


