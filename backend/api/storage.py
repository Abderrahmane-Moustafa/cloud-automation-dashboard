from fastapi import APIRouter, UploadFile, File, Form
import os
import shutil
import tempfile
from backend.services.aws_storage_service import upload_file_to_s3, list_files_in_s3
from backend.services.azure_storage_service import upload_file_to_azure, list_files_in_azure

router = APIRouter(prefix="/api/storage", tags=["Storage Operations"])

# Endpoint to upload a file to AWS S3
@router.post("/aws/upload")
async def upload_file(
    file: UploadFile = File(...),
    container_name: str = Form(...),
    object_name: str = Form(...)
):
    # Get temporary directory path
    temp_dir = tempfile.gettempdir()
    # Combine temp path with filename
    temp_path = os.path.join(temp_dir, file.filename)

    # Save the uploaded file to the temp path
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Upload saved file to S3 and remove local copy
    result = upload_file_to_s3(container_name, temp_path, object_name)
    os.remove(temp_path)

    return result

# Endpoint to list uploaded files in AWS S3
@router.get("/aws/list")
def list_uploaded_files(container_name: str):
    return {"files": list_files_in_s3(container_name)}


# Endpoint to upload a file to Azure Blob
@router.post("/azure/upload")
async def upload_file_azure(
    file: UploadFile = File(...),
    container_name: str = Form(...),
    object_name: str = Form(...)
):
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, file.filename)

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = upload_file_to_azure(container_name, temp_path, object_name)
    os.remove(temp_path)

    return result

# Endpoint to list uploaded files in Azure Blob
@router.get("/azure/list")
def list_uploaded_files_azure(container_name: str):
    return {"files": list_files_in_azure(container_name)}