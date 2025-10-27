# create_s3_bucket.py
import boto3
import random
import string
import os
from botocore.exceptions import ClientError

# --- Configuration ---
# Reads region from environment variables
AWS_REGION = os.getenv('AWS_REGION') or os.getenv('AWS_DEFAULT_REGION') or 'us-east-1' 

# --- Helper to generate a globally unique bucket name ---
def generate_unique_name(prefix='agriscale-photo-upload-'):
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefix}{random_suffix}"

S3_BUCKET_NAME = generate_unique_name()

print(f"Attempting to create S3 bucket: {S3_BUCKET_NAME} in region {AWS_REGION}")

try:
    # Initialize the S3 client (reads keys/region from environment)
    s3_client = boto3.client(
        's3',
        region_name=AWS_REGION
    )
    
    # 1. Bucket creation request
    # This will create the bucket with the default account-level Block Public Access setting.
    if AWS_REGION == 'us-east-1':
        s3_client.create_bucket(Bucket=S3_BUCKET_NAME)
    else:
        s3_client.create_bucket(Bucket=S3_BUCKET_NAME, CreateBucketConfiguration={'LocationConstraint': AWS_REGION})
    
    # --- CRITICAL FIX: REMOVED PUBLIC POLICY APPLICATION ---
    # The policy setting code has been removed entirely to bypass the Block Public Access error.
    
    print("\n✅ Success! Bucket created securely.")
    print("===============================================================")
    print(f"✅ BUCKET NAME TO USE IN APP/DB.PY: '{S3_BUCKET_NAME}'")
    print(f"✅ AWS REGION TO USE IN APP/DB.PY: '{AWS_REGION}'")
    print("===============================================================")

except ClientError as e:
    error_message = e.response['Error']['Message']
    print(f"\n❌ ERROR creating bucket: {error_message}")
    print("ACTION REQUIRED: Ensure your environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION) are set.")
except Exception as e:
    print(f"\n❌ An unexpected error occurred: {e}")