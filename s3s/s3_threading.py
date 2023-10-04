import boto3
import csv
import threading


def list_objects_and_save(bucket_name, csv_filename):
    # Initialize the S3 client
    s3 = boto3.client("s3")

    # Use the list_objects_v2 method to iterate through objects in the S3 bucket
    paginator = s3.get_paginator("list_objects_v2")

    # Initialize a list to store object details
    object_details = []

    try:
        # Function to list objects and add details to the object_details list
        def list_objects_to_csv(page):
            for obj in page.get("Contents", []):
                object_key = obj["Key"]
                object_size = obj["Size"]
                object_last_modified = obj["LastModified"].strftime("%Y-%m-%d %H:%M:%S")
                object_details.append([object_key, object_size, object_last_modified])

        # Iterate through the objects in the S3 bucket using threads
        threads = []
        for page in paginator.paginate(Bucket=bucket_name):
            thread = threading.Thread(target=list_objects_to_csv, args=(page,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Write object details to a CSV file
        with open(csv_filename, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Object Key", "Size (bytes)", "Last Modified"])
            csv_writer.writerows(object_details)

        print(f"Object details saved to {csv_filename}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    # Replace 'your-bucket-name' with your actual S3 bucket name
    bucket_name = "your-bucket-name"

    # Specify the CSV filename where you want to save the object details
    csv_filename = "object_details.csv"

    list_objects_and_save(bucket_name, csv_filename)
