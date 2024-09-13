# S3 to S3 Replication

To create a plan for AWS S3 content replication between two buckets, where changes in the destination bucket are replicated back to the original bucket, follow these steps:

### Step 1: Set Up Initial Replication from Source to Destination

1. **Create the S3 Buckets**:
   - Source bucket: `source-bucket`
   - Destination bucket: `destination-bucket`

2. **Enable Versioning** on both buckets to keep track of changes and support replication.

3. **Create an IAM Role** with the necessary permissions to allow S3 to perform replication. This role should have policies granting:
   - Read permissions on the source bucket.
   - Write permissions on the destination bucket.

4. **Configure Replication Rule** in the source bucket to replicate objects to the destination bucket:
   - Go to the source bucket in the S3 console.
   - Select the "Management" tab and then "Replication rules".
   - Create a new replication rule and configure it to replicate objects to the destination bucket.
   - Choose the IAM role created in the previous step.

### Step 2: Monitor and Replicate Changes Back to Source

1. **Set Up S3 Event Notifications** on the destination bucket to trigger a Lambda function upon object creation or modification:
   - Go to the destination bucket in the S3 console.
   - Select the "Properties" tab and then "Event notifications".
   - Create a new event notification for "All object create events".

2. **Create a Lambda Function** to handle replication back to the source bucket:
   - Write the Lambda function code to:
     - Get the modified object from the destination bucket.
     - Copy the object to the source bucket.
   - Assign the necessary IAM role to the Lambda function to allow read access to the destination bucket and write access to the source bucket.

### Lambda Function Example

Here's an example of the Lambda function code in Python (using Boto3):

```python
import boto3
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    for record in event['Records']:
        destination_bucket = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']

        # Copy object from destination bucket to source bucket
        copy_source = {'Bucket': destination_bucket, 'Key': object_key}
        source_bucket = 'source-bucket'
        
        try:
            s3.copy_object(CopySource=copy_source, Bucket=source_bucket, Key=object_key)
            print(f"Copied {object_key} from {destination_bucket} to {source_bucket}")
        except Exception as e:
            print(f"Error copying object: {str(e)}")
```

### Step 3: Test the Setup

1. **Upload an Object to the Source Bucket**:
   - Verify it gets replicated to the destination bucket.

2. **Modify the Object in the Destination Bucket**:
   - Verify the modified object gets replicated back to the source bucket.

### Step 4: Monitoring and Maintenance

1. **Enable Logging** and **Metrics** for both buckets to monitor replication status and performance.
2. **Regularly Review** IAM policies and roles to ensure they follow the principle of least privilege.
3. **Set Up Alerts** using Amazon CloudWatch to notify you of any replication failures or issues.

### Diagram (Optional)

Consider creating a visual diagram for better understanding:
1. Source Bucket → Destination Bucket (initial replication).
2. Destination Bucket → Source Bucket (change replication via Lambda).

This plan should ensure bi-directional synchronization between the two S3 buckets while maintaining simplicity and reliability.


# With Terraform code

Here's a Terraform script to set up the AWS S3 content replication between two buckets with the described requirements. This script includes creating the necessary S3 buckets, enabling versioning, configuring the IAM roles and policies, setting up replication rules, and creating a Lambda function to handle the replication back from the destination to the source bucket.

### Prerequisites

Ensure you have Terraform installed and configured to use your AWS credentials.

### Terraform Script

```hcl
provider "aws" {
  region = "us-east-1" # Change this to your preferred region
}

resource "aws_s3_bucket" "source_bucket" {
  bucket = "source-bucket"
  versioning {
    enabled = true
  }
}

resource "aws_s3_bucket" "destination_bucket" {
  bucket = "destination-bucket"
  versioning {
    enabled = true
  }
}

resource "aws_iam_role" "s3_replication_role" {
  name = "s3-replication-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "s3.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "s3_replication_policy" {
  name   = "s3-replication-policy"
  role   = aws_iam_role.s3_replication_role.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:GetObjectVersionForReplication",
          "s3:GetObjectVersionAcl",
          "s3:GetObjectVersionTagging",
          "s3:ListBucket"
        ],
        Resource = [
          aws_s3_bucket.source_bucket.arn,
          "${aws_s3_bucket.source_bucket.arn}/*"
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "s3:ReplicateObject",
          "s3:ReplicateDelete",
          "s3:ReplicateTags"
        ],
        Resource = [
          aws_s3_bucket.destination_bucket.arn,
          "${aws_s3_bucket.destination_bucket.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_s3_bucket_replication_configuration" "source_to_destination" {
  bucket = aws_s3_bucket.source_bucket.id
  role   = aws_iam_role.s3_replication_role.arn

  rule {
    id     = "source-to-destination"
    status = "Enabled"

    filter {
      prefix = ""
    }

    destination {
      bucket        = aws_s3_bucket.destination_bucket.arn
      storage_class = "STANDARD"
    }
  }
}

resource "aws_lambda_function" "replication_function" {
  function_name = "replication-function"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "index.lambda_handler"
  runtime       = "python3.9"
  filename      = "lambda.zip"

  source_code_hash = filebase64sha256("lambda.zip")
}

resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.replication_function.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.destination_bucket.arn
}

resource "aws_s3_bucket_notification" "destination_bucket_notification" {
  bucket = aws_s3_bucket.destination_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.replication_function.arn
    events              = ["s3:ObjectCreated:*"]
  }
}

resource "aws_iam_role" "lambda_exec" {
  name = "lambda-exec"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  name   = "lambda-policy"
  role   = aws_iam_role.lambda_exec.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ],
        Resource = [
          "${aws_s3_bucket.source_bucket.arn}/*",
          "${aws_s3_bucket.destination_bucket.arn}/*"
        ]
      },
      {
        Effect = "Allow",
        Action = "logs:*",
        Resource = "*"
      }
    ]
  })
}

# Lambda function code in a file named index.py
# Zip the file to lambda.zip before applying the Terraform script
/*
index.py
---------
import boto3
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    for record in event['Records']:
        destination_bucket = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']

        # Copy object from destination bucket to source bucket
        copy_source = {'Bucket': destination_bucket, 'Key': object_key}
        source_bucket = 'source-bucket'
        
        try:
            s3.copy_object(CopySource=copy_source, Bucket=source_bucket, Key=object_key)
            print(f"Copied {object_key} from {destination_bucket} to {source_bucket}")
        except Exception as e:
            print(f"Error copying object: {str(e)}")
*/
```

### Instructions

1. Save the above Terraform code to a file named `main.tf`.
2. Create a Python file named `index.py` with the provided Lambda function code.
3. Zip the `index.py` file to create `lambda.zip`.
4. Run the following commands in your terminal:

```sh
terraform init
terraform apply
```

This script sets up the S3 buckets, IAM roles, replication rules, and Lambda function to achieve the desired replication behavior. Make sure to adapt the bucket names and region as per your requirements.