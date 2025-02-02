import boto3
import os
from botocore.exceptions import ClientError

# Initialize S3 client
s3_client = boto3.client('s3', region_name='us-west-2')

# Define bucket and file details
bucket_name = "my-generative-ai-bucket-12345"  # Replace with your bucket name
local_file_path = r"S3\data\database.sqlite"  # Replace with your file path
s3_object_name = "data.sqlite"  # Name in S3
part_size = 5 * 1024 * 1024  # 5MB per part

def multipart_upload():
    """Uploads a large file to S3 using multipart upload."""
    try:
        # Step 1: Initiate multipart upload
        response = s3_client.create_multipart_upload(Bucket=bucket_name, Key=s3_object_name)
        upload_id = response["UploadId"]
        print(f"Multipart upload initiated: Upload ID = {upload_id}")

        # Step 2: Upload file parts
        parts = []
        with open(local_file_path, "rb") as file:
            part_number = 1
            while chunk := file.read(part_size):
                response = s3_client.upload_part(
                    Bucket=bucket_name,
                    Key=s3_object_name,
                    PartNumber=part_number,
                    UploadId=upload_id,
                    Body=chunk
                )
                parts.append({"PartNumber": part_number, "ETag": response["ETag"]})
                print(f"Uploaded part {part_number}")
                part_number += 1

        # Step 3: Complete multipart upload
        s3_client.complete_multipart_upload(
            Bucket=bucket_name,
            Key=s3_object_name,
            UploadId=upload_id,
            MultipartUpload={"Parts": parts}
        )
        print(f"Multipart upload completed successfully!")

    except ClientError as e:
        print(f"Error: {e}")
        # Abort upload if an error occurs
        s3_client.abort_multipart_upload(Bucket=bucket_name, Key=s3_object_name, UploadId=upload_id)
        print("Multipart upload aborted.")

multipart_upload()
