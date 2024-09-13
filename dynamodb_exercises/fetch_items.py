import boto3
import asyncio


class DataFetcher:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.s3 = boto3.client('s3')

    def fetch_dynamodb_records(self, table_name, batch_size=100):
        table = self.dynamodb.Table(table_name)
        response = table.query(Limit=batch_size)
        data = response.get('Items', [])

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'], Limit=batch_size)
            data.extend(response.get('Items', []))

        return data

    async def fetch_s3_objects(self, bucket_name, prefix=''):
        loop = asyncio.get_event_loop()
        paginator = self.s3.get_paginator('list_objects_v2')

        result = []
        async for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
            result.extend(page.get('Contents', []))

        return result


# Example usage
async def main():
    fetcher = DataFetcher()
    dynamodb_data = fetcher.fetch_dynamodb_records('your-table-name')
    s3_data = await fetcher.fetch_s3_objects('your-bucket-name', 'your-prefix')
    print(f"DynamoDB Records: {len(dynamodb_data)}")
    print(f"S3 Objects: {len(s3_data)}")


asyncio.run(main())
