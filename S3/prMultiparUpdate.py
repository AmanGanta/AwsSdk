import boto3
import os
import concurrent.futures
from botocore.exceptions import ClientError

# Initialize S3 client
s3_client = boto3.client('s3', region_name='us-west-2')

# Define bucket and file details
bucket_name = "my-generative-ai-bucket-12345"  # Replace with your bucket name
local_file_path = r"S3\data\database.sqlite"  # Replace with your file path
s3_object_name = "data.sqlite"  # Name in S3
part_size = 5 * 1024 * 1024  # 5MB per part

def upload_part(part_number, data, upload_id):
    """Uploads a single part in parallel."""
    try:
        response = s3_client.upload_part(
            Bucket=bucket_name,
            Key=s3_object_name,
            PartNumber=part_number,
            UploadId=upload_id,
            Body=data
        )
        print(f"Uploaded part {part_number}")
        return {"PartNumber": part_number, "ETag": response["ETag"]}
    except ClientError as e:
        print(f"Error uploading part {part_number}: {e}")
        return None

def multipart_upload():
    """Uploads a large file to S3 using parallel multipart upload."""
    try:
        # Step 1: Initiate multipart upload
        response = s3_client.create_multipart_upload(Bucket=bucket_name, Key=s3_object_name)
        upload_id = response["UploadId"]
        print(f"Multipart upload initiated: Upload ID = {upload_id}")

        # Step 2: Read file and prepare parts
        parts = []
        with open(local_file_path, "rb") as file:
            part_number = 1
            chunks = []
            while chunk := file.read(part_size):
                chunks.append((part_number, chunk, upload_id))
                part_number += 1

        # Step 3: Upload parts in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(lambda p: upload_part(*p), chunks)
        
        # Collect successful uploads
        parts = [part for part in results if part]

        # Step 4: Complete multipart upload
        if parts:
            s3_client.complete_multipart_upload(
                Bucket=bucket_name,
                Key=s3_object_name,
                UploadId=upload_id,
                MultipartUpload={"Parts": parts}
            )
            print(f"Multipart upload completed successfully!")
        else:
            raise Exception("No parts were successfully uploaded.")

    except ClientError as e:
        print(f"Error: {e}")
        s3_client.abort_multipart_upload(Bucket=bucket_name, Key=s3_object_name, UploadId=upload_id)
        print("Multipart upload aborted.")

multipart_upload()
