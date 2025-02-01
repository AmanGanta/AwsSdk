import boto3
from botocore.exceptions import ClientError

# Initialize IAM client
iam_client = boto3.client('iam')

# Step 1: Create an IAM User
try:
    user_name = "MyGenerativeAIUser"  # Replace with your desired username
    response = iam_client.create_user(UserName=user_name)
    print(f"IAM User '{user_name}' created successfully!")
except ClientError as e:
    print(f"Error creating user: {e}")

# Step 2: Attach a Policy to the User
try:
    policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"  # Example policy
    iam_client.attach_user_policy(UserName=user_name, PolicyArn=policy_arn)
    print(f"Policy '{policy_arn}' attached to user '{user_name}'!")
except ClientError as e:
    print(f"Error attaching policy: {e}")

# Step 3: Create Access Keys for Programmatic Access
try:
    access_key_response = iam_client.create_access_key(UserName=user_name)
    access_key_id = access_key_response['AccessKey']['AccessKeyId']
    secret_access_key = access_key_response['AccessKey']['SecretAccessKey']
    print(f"Access Key ID: {access_key_id}")
    print(f"Secret Access Key: {secret_access_key}")
except ClientError as e:
    print(f"Error creating access keys: {e}")
