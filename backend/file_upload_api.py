from fastapi import FastAPI, File, UploadFile, Response
import boto3
import botocore
import os
from botocore.exceptions import NoCredentialsError
from fastapi import FastAPI, File, UploadFile, HTTPException

app = FastAPI()

# Define your S3 credentials

aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
s3_bucket = os.environ.get('S3_BUCKET')
region_name = os.environ.get('S3_REGION')

# Create a new S3 client
s3 = boto3.client('s3', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Define function to upload file to S3
@app.post("/uploadfile/")
def upload_to_aws(local_file, s3_file: str) -> dict:
    folder = 'adhocprocess/'
    s3_file = folder + s3_file
    try:
        s3.upload_fileobj(local_file, s3_bucket, s3_file)
        return {"success": True}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found.")
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="Credentials not available.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred while uploading file to S3: {e}")

# @app.post("/uploadfile/")
# async def upload_file(file: UploadFile = File(...), s3_file: str = ""):
#     folder = 'adhocprocess/'
#     s3_file = folder + s3_file
#     content = await file.read()
#     result = s3.upload_fileobj(content, s3_bucket, s3_file)
#     # result = upload_to_aws(content, s3_file)
#     if result["success"]:
#         return {"success": True}
#     else:
#         raise HTTPException(status_code=500, detail="Error occurred while uploading file to S3.")
  

    
@app.get("/downloadfile/{file_name}")
async def download_file(file_name: str, response: Response):
    """
    Downloads a file from an S3 bucket.
    """
    try:
        # Create a key for the file in the S3 bucket
        key = f"uploads/{file_name}"
        
        # Download the file from S3
        response.headers["Content-Disposition"] = f"attachment; filename={file_name}"
        s3.download_fileobj(s3_bucket, key, response.body)
        return response
    except botocore.exceptions.ParamValidationError as e:
        return {"error": f"Parameter validation error: {e}"}
    except botocore.exceptions.ClientError as e:
        return {"error": f"Client error: {e}"}
