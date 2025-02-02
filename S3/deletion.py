import boto3
from botocore.exceptions import ClientError

s3 = boto3.resource('s3', region_name='us-west-2')

# Define bucket name (must be globally unique)
bucket_name = "my-generative-ai-bucket-12345"  # Change to a unique name
bucket = s3.Bucket(bucket_name)

# Define file details
s3_object_name = "example.txt" 

try:
    for obj in bucket.objects.all():
        obj.delete()
    print(f"All objects deleted from '{bucket_name}'!")

    # Step 2: Delete the bucket
    # bucket.delete()
    # print(f"S3 bucket '{bucket_name}' deleted successfully!")

except ClientError as e:
    print(f"Error: {e}")
