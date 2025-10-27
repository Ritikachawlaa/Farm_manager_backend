# set_s3_cors.py
import boto3
from botocore.exceptions import ClientError
import os
import json

# --- CONFIGURATION (Match your current setup) ---
S3_BUCKET_NAME = "agriscale-photo-upload-um7riwja" # <<< Use your exact bucket name
AWS_REGION = 'us-east-1' # <<< Use your exact region
# -----------------------------------------------

# Define the CORS policy to allow uploads from your local development server (8080)
cors_configuration = {
    'CORSRules': [
        {
            # Rule 1: Allow all necessary methods (PUT/POST for upload, GET/HEAD for presign checks)
            'AllowedHeaders': ['*'],
            'AllowedMethods': ['GET', 'PUT', 'POST', 'HEAD'], 
            'AllowedOrigins': [
                'http://localhost:8080',  # The primary dev port
                'http://localhost:3000',  # Common dev port
                'http://localhost:8081',  # Alternate dev port
                'http://127.0.0.1:8080',  # 127.0.0.1 variants
                # Add your production domain later: 'https://app.yourdomain.com'
            ],
            # Allow all headers to pass
            'ExposeHeaders': [],
            # MaxAgeSeconds is optional but recommended
            'MaxAgeSeconds': 3000
        }
    ]
}

print(f"Attempting to set CORS policy on bucket: {S3_BUCKET_NAME}")

try:
    # Boto3 client initialization (reads keys/region from environment)
    s3_client = boto3.client(
        's3',
        region_name=AWS_REGION
    )
    
    # Apply the CORS configuration
    s3_client.put_bucket_cors(
        Bucket=S3_BUCKET_NAME,
        CORSConfiguration=cors_configuration
    )
    
    print("\n✅ Success! CORS policy applied to S3 bucket.")
    print("Your frontend on localhost:8080 can now upload files directly.")

except ClientError as e:
    error_message = e.response['Error']['Message']
    print(f"\n❌ ERROR applying CORS policy: {error_message}")
    print("ACTION REQUIRED: Ensure your AWS IAM User has 's3:PutBucketCORS' permissions for this bucket.")
except Exception as e:
    print(f"\n❌ An unexpected error occurred: {e}")