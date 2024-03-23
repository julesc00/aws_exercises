import boto3
from datetime import datetime
from dateutil.tz import tzutc


def list_bucket_items_by_timestamp(bucket_name):
    # Create an S3 client
    s3 = boto3.client("s3")

    objs = [
        {
            "Key": "etl/alphasense/simon_mail/events/2024/02/21/18/alphasense_simon_mail_events_2024-02-21-06-53-888966-976d2200-4b3e-4c9b-9dcf-815ed0614141",
            "LastModified": datetime(2024, 2, 20, 18, 2, 7, tzinfo=tzutc()),
            "ETag": '"2b5e4eb299b4175b8978fdf599a15b84"',
            "Size": 2258,
            "StorageClass": "STANDARD",
        }
    ]
    last_timestamps = [datetime(2024, 2, 20, 18, 2, 7, tzinfo=tzutc())]
    last_existing_timestamp = None
    # List objects in the bucket
    response = s3.list_objects_v2(
        Bucket=bucket_name, Prefix="etl/alphasense/simon_mail/events/2024/02/21/18/"
    )

    # Extract and sort objects based on their LastModified timestamp
    if "Contents" in response:
        if not objs:
            print("No previous objects in the list. Adding the first batch.")
            objs = sorted(response["Contents"], key=lambda obj: obj["LastModified"])
            last_timestamps.append(objs[-1])

        elif objs:
            print("Objects found in the list. Adding the next batch.")
            tmp_objs = sorted(response["Contents"], key=lambda obj: obj["LastModified"])
            objs += tmp_objs
            last_timestamps.append(tmp_objs[-1])

    else:
        print("No objects found in the bucket.")

    last_processed_with_timestamp = max(objs, key=lambda obj: obj["LastModified"])

    before_last_processed_with_timestamp = objs[-2]["LastModified"]
    last_timestamp = last_processed_with_timestamp["LastModified"]
    print(
        f"Timestamps higher than?: {last_timestamp < before_last_processed_with_timestamp}"
    )
    print(
        f"timestamps types: {type(last_timestamp), type(before_last_processed_with_timestamp)}"
    )
    print(last_timestamp)
    print(before_last_processed_with_timestamp)

    print(f"Number of objects: {len(objs)}")
    print(f"Type of container: {type(objs)}")
    print(f"Existing objects: {objs[0]}")
    print(f"Second last object: {objs[-2]}")
    print(f"Last object: {objs[-1]}")

    print(
        f"Previous existing timestamp: {last_timestamps[-2] if len(last_timestamps) > 1 else last_timestamps[-1]}"
    )
    print(f"Last processed object: {last_processed_with_timestamp['LastModified']}")
    print(
        "No previous one, this is first"
        if last_existing_timestamp == last_processed_with_timestamp
        else "There is a previous one"
    )
    print(last_existing_timestamp == last_processed_with_timestamp)
    print(f"Number of timestamps: {len(last_timestamps)}")
    return objs, len(objs)


# Example usage:
bucket_name = "data.simondata.com"
print(list_bucket_items_by_timestamp(bucket_name))
