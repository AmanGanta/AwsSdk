import boto3
from botocore.exceptions import ClientError

# Initialize S3 client
s3_client = boto3.client('s3', region_name='us-west-2')

# Define the bucket name
bucket_name = "my-generative-ai-bucket-12345"  # Replace with your bucket name

try:
    # List objects in the bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    
    # Check if the bucket has files
    if "Contents" in response:
        print("Files in S3 Bucket:")
        for obj in response["Contents"]:
            print(f"- {obj['Key']} (Size: {obj['Size']} bytes, Last Modified: {obj['LastModified']})")
    else:
        print("Bucket is empty.")

except ClientError as e:
    print(f"Error listing files: {e}")

# response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix="data/", MaxKeys=100)

# if "Contents" in response:
#     for obj in response["Contents"]:
#         if obj["Key"].endswith(".txt"):
#             print(f"- {obj['Key']} (Size: {obj['Size']} bytes)")