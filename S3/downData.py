import boto3
from botocore.exceptions import ClientError

# Initialize S3 client
s3_client = boto3.client('s3', region_name='us-west-2')

# Define variables
bucket_name = "my-generative-ai-bucket-12345"  # Replace with your bucket name
s3_object_name = "uploaded-example.txt"  # Name of the file in S3
local_download_path =r"S3\data\a.txt"  # Change this to where you want to save the file

try:
    # Download the file from S3
    s3_client.download_file(bucket_name, s3_object_name, local_download_path)
    print(f"File '{s3_object_name}' downloaded successfully to '{local_download_path}'!")
except ClientError as e:
    print(f"Error downloading file: {e}")
local_download_path =r"S3\data\b.txt" 
try:
    with open(local_download_path, 'wb') as f:
        s3_client.download_fileobj(bucket_name, s3_object_name, f)
except ClientError as e:
    print(f"Error downloading file: {e}")


    