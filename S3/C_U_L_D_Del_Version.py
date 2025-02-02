import boto3
from botocore.exceptions import ClientError

# Initialize S3 client and resource
s3_client = boto3.client('s3', region_name='us-west-2')
s3 = boto3.resource('s3', region_name='us-west-2')

# Define bucket name (must be globally unique)
bucket_name = "my-generative-ai-bucket-12345"  # Change to a unique name
bucket = s3.Bucket(bucket_name)

# Define file details
local_file_path = "S3\data\\b.txt"  # Replace with your file path
s3_object_name = "example.txt"  # Object key in S3


def create_versioned_bucket():
    """Create an S3 bucket and enable versioning."""
    try:
        # Step 1: Create S3 bucket
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'us-west-2'}
        )
        print(f"S3 Bucket '{bucket_name}' created successfully!")

        # Step 2: Enable versioning
        s3_client.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={'Status': 'Enabled'}
        )
        print(f"Versioning enabled for bucket: {bucket_name}")

    except ClientError as e:
        print(f"Error creating bucket: {e}")


def upload_file():
    """Upload a file multiple times to create different versions."""
    try:
        for i in range(3):  # Upload 3 versions of the same file
            s3_client.upload_file(local_file_path, bucket_name, s3_object_name)
            print(f"Uploaded version {i+1} of '{s3_object_name}'")
    except ClientError as e:
        print(f"Error uploading file: {e}")


def list_versions():
    """List all versions of a file in the bucket."""
    try:
        response = s3_client.list_object_versions(Bucket=bucket_name, Prefix=s3_object_name)
        if "Versions" in response:
            print(f"Versions of '{s3_object_name}':")
            for version in response["Versions"]:
                print(f"- Version ID: {version['VersionId']} (Last Modified: {version['LastModified']})")
        else:
            print(f"No versions found for '{s3_object_name}'.")
    except ClientError as e:
        print(f"Error listing versions: {e}")


def download_specific_version(version_id, download_path):
    """Download a specific version of a file."""
    try:
        s3_client.download_file(bucket_name, s3_object_name, download_path, ExtraArgs={'VersionId': version_id})
        print(f"Downloaded version {version_id} of '{s3_object_name}' to '{download_path}'")
    except ClientError as e:
        print(f"Error downloading version: {e}")


def delete_all_objects_and_bucket():
    """Delete all objects (including versions) and remove the bucket."""
    try:
        # Step 1: Delete all standard objects
        for obj in bucket.objects.all():
            obj.delete()
        print(f"All standard objects deleted from '{bucket_name}'!")

        # Step 2: Check if versioning is enabled
        versioning_status = s3_client.get_bucket_versioning(Bucket=bucket_name)
        if versioning_status.get("Status") == "Enabled":
            # Step 3: Delete all versioned objects
            for obj_version in bucket.object_versions.all():
                obj_version.delete()
            print(f"All versioned objects deleted from '{bucket_name}'!")

        # Step 4: Delete the bucket
        #bucket.delete()
        #print(f"S3 bucket '{bucket_name}' deleted successfully!")

    except ClientError as e:
        print(f"Error: {e}")


# **Execution Flow**
if __name__ == "__main__":
    #create_versioned_bucket()  # Step 1: Create bucket and enable versioning
    #upload_file()              # Step 2: Upload multiple versions
    delete_all_objects_and_bucket()
    list_versions()            # Step 3: List available versions

    # Example: Download a specific version (manually input a version ID after listing)
    # version_id = "ENTER_VERSION_ID_HERE"
    # download_specific_version(version_id, "C:\\Users\\YourName\\Downloads\\downloaded-version.txt")

    # Cleanup: Delete all objects & bucket (run this when you want to remove everything)
    # delete_all_objects_and_bucket()
