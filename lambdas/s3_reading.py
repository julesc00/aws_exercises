import json
import boto3

client = boto3.client("s3")
db_client = boto3.client("dynamodb")
resource = boto3.resource("dynamodb")

s3_error = client.exceptions

"""
1. Create DynamoDB table
2. Get bucket object (JSON file)
3. Write items to table.
NOTE: Serialize/Deserialize json < -- > dict
    loads()
    JSON to dict
    x = json.loads(json_var)
    
    dumps()
    dict to JSON
    x = json.dumps(dict_var)
"""


def lambda_handler(event, context):
    table_name = "user_data"

    # 1. Create DynamoDB table
    create_dynamodb_table(resource, table_name)

    # 2. Read JSON data sample from S3 bucket
    response = get_s3_object(client, "bucket_name", "sample_user_data.json")

    # Convert from streaming data to bytes
    json_data = response["Body"].read()
    data_str = json_data.decode("UTF-8")

    # JSON to dict
    data_dict = json.loads(data_str)

    # 3. Insert one item data into DynamoDB
    write_dynamodb_item(resource, table_name, data_dict)

    # 4. List tables
    table_lst = list(resource.tables.all())
    print(table_lst)
    return {
        "statusCode": 200,
        "message": json.dumps("Things went good")
    }


def get_s3_object(aws_client, bucket_name: str, file_key_name: str):
    try:
        response = aws_client.get_object(
            Bucket=bucket_name,
            Key=file_key_name
        )
        return response
    except aws_client.exceptions.ResourceNotExistError as e:
        print(e)
        pass


def create_dynamodb_table(aws_resource, table_name: str):
    try:
        table = aws_resource.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    "AttributeName": "user_name",
                    "KeyType": "HASH"
                },
                {
                    "AttributeName": "city",
                    "KeyType": "RANGE"
                },
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "user_name",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "city",
                    "AttributeType": "S"
                },
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        )

        # Wait until table exists
        table.wait_until_exists()
    except db_client.exceptions.ResourceInUseException as e:
        print(e)
        pass


def write_dynamodb_item(aws_resource, table_name: str, data: dict):
    try:
        table = aws_resource.Table(table_name)
        table.put_item(
            Item=data
        )
        return table
    except ValueError as e:
        return e
