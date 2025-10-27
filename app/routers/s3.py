# agriscale_backend/app/routers/s3.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from .. import db # Import db for bucket name
import uuid
import os
from .. import db

router = APIRouter(
    prefix="/s3",
    tags=["S3 Upload"]
)

# Pydantic model for the request payload
class UploadRequest(BaseModel):
    file_name: str = Field(..., description="The original name of the file.")
    file_type: str = Field(..., description="The MIME type of the file (e.g., image/jpeg).")

# Pydantic model for the response payload
class UploadResponse(BaseModel):
    # Adjusted response to include fields for POST method
    upload_url: str
    file_key: str 
    fields: dict 

@router.post("/generate-upload-url", response_model=UploadResponse)
async def generate_upload_url(request: UploadRequest):
    """
    Generates a secure, temporary pre-signed URL for the client to POST a file directly to S3.
    """
    bucket_name = db.S3_BUCKET_NAME

    if bucket_name == "YOUR_UNIQUE_S3_BUCKET_NAME":
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                             detail="S3 Bucket name not configured in app/db.py")

    # Define the file key (path in S3)
    file_extension = os.path.splitext(request.file_name)[1]
    # Creates a path like: supervisors/uuid.jpg
    file_key = f"supervisors/{uuid.uuid4()}{file_extension}" 

    try:
        # Boto3 will find credentials automatically
        s3_client = boto3.client('s3', config=Config(signature_version='s3v4'))
        
        # Generate the presigned POST data
        presigned_post = s3_client.generate_presigned_post(
            Bucket=bucket_name,
            Key=file_key,
            Fields={"Content-Type": request.file_type},
            Conditions=[{"Content-Type": request.file_type}],
            ExpiresIn=600 # URL expires in 10 minutes
        )
        
        # Return the URL and necessary fields for the frontend to post the file
        return {
            "upload_url": presigned_post['url'],
            "file_key": file_key,
            "fields": presigned_post['fields']
        }
        
    except ClientError as e:
        error_message = e.response.get('Error', {}).get('Message', 'AWS S3 Client Error')
        print(f"S3 Client Error: {error_message}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"S3 Error: {error_message}")
    except Exception as e:
        print(f"Unexpected error generating URL: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not generate upload URL.")
    
@router.get("/get-photo-url", response_model=str)
async def get_photo_url(file_key: str):
    """
    Generates a secure, temporary pre-signed URL for the client to GET (view) a private S3 object.
    """
    bucket_name = db.S3_BUCKET_NAME
    region_name = db.AWS_REGION
    
    if not file_key:
        raise HTTPException(status_code=400, detail="file_key parameter is required.")

    try:
        s3_client = boto3.client(
            's3',
            region_name=region_name,
            config=Config(signature_version='s3v4')
        )
        
        # Generate the presigned URL for a GET operation (viewing the image)
        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': bucket_name,
                'Key': file_key 
            },
            ExpiresIn=3600 # URL expires in 1 hour
        )
        
        return url
        
    except ClientError as e:
        print(f"S3 Client Error getting URL: {e}")
        raise HTTPException(status_code=500, detail="Could not generate secure photo URL.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Server error during URL generation.")

# ... (Keep your existing generate-upload-url PO