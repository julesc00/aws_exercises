import json
import threading
import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('your-table-name')


def fetch_dynamodb_data(partition_key):
    """
    Function to fetch data from DynamoDB table based on partition key.
    """
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('partition_key').eq(partition_key)
    )
    return response['Items']


def thread_worker(partition_key, results, index):
    """
    Thread worker function to fetch data and store results in the shared list.
    """
    results[index] = fetch_dynamodb_data(partition_key)


def lambda_handler(event, context):
    partition_keys = event.get('partition_keys', [])  # List of partition keys to fetch data for
    threads = []
    results = [None] * len(partition_keys)  # Shared list to store results from each thread

    # Create and start a thread for each partition key
    for i, partition_key in enumerate(partition_keys):
        thread = threading.Thread(target=thread_worker, args=(partition_key, results, i))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }


# Example event to test the Lambda function locally
if __name__ == "__main__":
    test_event = {
        'partition_keys': ['partition1', 'partition2', 'partition3']
    }
    print(lambda_handler(test_event, None))
