import boto3
from botocore.exceptions import ClientError

# Initialize S3 client
s3_client = boto3.client('s3', region_name='us-west-2')

# Define variables
bucket_name = "my-generative-ai-bucket-12345"  # Replace with your bucket name
local_file_path = r"S3/data/a.txt"  # Replace with your file path
s3_object_name = "uploaded-example3.txt"  # The name to store the file as in S3

try:
    # Upload the file
    s3_client.upload_file(local_file_path, bucket_name, s3_object_name)
    print(f"File '{local_file_path}' uploaded successfully as '{s3_object_name}' in '{bucket_name}'!")
except ClientError as e:
    print(f"Error uploading file: {e}")
