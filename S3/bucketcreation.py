import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client('s3', region_name='us-west-2')

bucket_name = "my-generative-ai-bucket-12345"  # Change to a unique name

try:
    response = s3_client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={'LocationConstraint': 'us-west-2'},
        ACL='private',  # Ensures only the bucket owner has access
        ObjectLockEnabledForBucket=True  # Enables object lock for compliance
    )
    print(f"Secure S3 Bucket '{bucket_name}' created successfully!")
except ClientError as e:
    print(f"Error creating bucket: {e}")
