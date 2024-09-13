# Instructions to configure S3 to S3 replication using the AWS Management Console:

## Step 1: Set Up Initial Replication from Source to Destination
1. **Create the S3 Buckets**:
   - Source bucket: `source-bucket`
   - Destination bucket: `destination-bucket`
   - Note: Ensure that versioning is enabled on both buckets.
2. **Create Bucket Replication Rule**:
![pic1](img/Screenshot%20from%202024-08-02%2013-35-44.png)
3. **Tip**: Run `aws sync` command to copy the existing objects from the source bucket to the destination bucket.
   - **Note**: I had to create the policy with the Policy helper `Add Statement` option to get the correct policy.
4. **Monitor Replication**:
   - Go to the `Management` tab of the source bucket.
   - Click on the `Replication` option to monitor the replication status.