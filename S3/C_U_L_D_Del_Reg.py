import boto3
from botocore.exceptions import ClientError

# Initialize S3 client and resource
s3_client = boto3.client('s3', region_name='us-west-2')
s3 = boto3.resource('s3', region_name='us-west-2')

# Define bucket name (must be globally unique)
bucket_name = "my-generative-ai-bucket-12345"  # Change to a unique name
bucket = s3.Bucket(bucket_name)

# Define file details
local_file_path = "C:\\Users\\YourName\\Documents\\example.txt"  # Replace with your file path
s3_object_name = "example.txt"  # Object key in S3


def create_bucket():
    """Create a standard S3 bucket (non-versioned)."""
    try:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'us-west-2'}
        )
        print(f"S3 Bucket '{bucket_name}' created successfully!")
    except ClientError as e:
        print(f"Error creating bucket: {e}")


def upload_file():
    """Upload a file to the S3 bucket."""
    try:
        s3_client.upload_file(local_file_path, bucket_name, s3_object_name)
        print(f"File '{s3_object_name}' uploaded successfully!")
    except ClientError as e:
        print(f"Error uploading file: {e}")


def list_files():
    """List all files in the S3 bucket."""
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if "Contents" in response:
            print(f"Files in bucket '{bucket_name}':")
            for obj in response["Contents"]:
                print(f"- {obj['Key']} (Size: {obj['Size']} bytes, Last Modified: {obj['LastModified']})")
        else:
            print(f"Bucket '{bucket_name}' is empty.")
    except ClientError as e:
        print(f"Error listing files: {e}")


def download_file(download_path):
    """Download a file from the S3 bucket."""
    try:
        s3_client.download_file(bucket_name, s3_object_name, download_path)
        print(f"File '{s3_object_name}' downloaded successfully to '{download_path}'")
    except ClientError as e:
        print(f"Error downloading file: {e}")


def delete_all_objects_and_bucket():
    """Delete all objects and remove the bucket."""
    try:
        # Step 1: Delete all objects
        for obj in bucket.objects.all():
            obj.delete()
        print(f"All objects deleted from '{bucket_name}'!")

        # Step 2: Delete the bucket
        bucket.delete()
        print(f"S3 bucket '{bucket_name}' deleted successfully!")

    except ClientError as e:
        print(f"Error: {e}")


# **Execution Flow**
if __name__ == "__main__":
    create_bucket()              # Step 1: Create a standard bucket
    upload_file()                # Step 2: Upload a file
    list_files()                 # Step 3: List all files

    # Example: Download a file
    # download_file("C:\\Users\\YourName\\Downloads\\downloaded-example.txt")

    # Cleanup: Delete all files & bucket (run this when you want to remove everything)
    # delete_all_objects_and_bucket()
