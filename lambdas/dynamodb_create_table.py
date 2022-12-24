import json
import boto3

db = boto3.resource("dynamodb")


def lambda_handler(event, context):
    table_name = "RetailSales-12232023"
    table = db.Table(table_name)
    # Write multiple items to table
    table.update_item(
        Key={
            "CustomerID": "A007",
            "Product": "Ferrari California"
        },
        UpdateExpression="SET product = :val1",
        ExpressionAttributeValues={":val1": "Guayina"}
    )


def create_table(resource, table_name):
    response = resource.create_table(
        AttributeDefinitions=[
            {
                "AttributeName": "CustomerID",
                "AttributeType": "S"
            },
            {
                "AttributeName": "Product",
                "AttributeType": "S"
            }
        ],
        TableName=table_name,
        KeySchema=[
            {
                "AttributeName": "CustomerID",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "Product",
                "KeyType": "RANGE"
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1
        }
    )
    return response[""]


def create_items(table):
    response =


