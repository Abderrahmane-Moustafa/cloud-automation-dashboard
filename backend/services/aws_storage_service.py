from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver
from backend.config.settings import settings
from backend.utils.logger import logger  # ← Logging


# Upload file to AWS S3 bucket
def upload_file_to_s3(container_name: str, file_path: str, object_name: str):
    logger.info(f"Uploading file to AWS S3: container={container_name}, object_name={object_name}")

    cls = get_driver(Provider.S3)
    driver = cls(settings.aws_access_key, settings.aws_secret_key)

    # Get container (S3 bucket) by name
    try:
        container = driver.get_container(container_name)
    except Exception as e:
        logger.error(f"Failed to access S3 bucket '{container_name}': {e}")
        return {"error": f"Cannot access bucket '{container_name}' - {e}"}

    # Upload file from local path to the container
    try:
        obj = driver.upload_object(
            file_path=file_path,
            container=container,
            object_name=object_name
        )
        logger.info(f"Uploaded file '{object_name}' to AWS S3 bucket '{container_name}'")
        return {
            "object_name": obj.name,
            "size": obj.size,
            "url": obj.extra.get("object_uri", "N/A")
        }
    except Exception as e:
        logger.error(f"Failed to upload file '{object_name}' to S3: {e}")
        return {"error": f"Upload failed - {e}"}


# List files inside a specific S3 bucket
def list_files_in_s3(container_name: str):
    logger.info(f"Listing files in AWS S3 bucket: {container_name}")

    cls = get_driver(Provider.S3)
    driver = cls(settings.aws_access_key, settings.aws_secret_key)

    try:
        container = driver.get_container(container_name)
        objects = driver.list_container_objects(container)
        logger.info(f"Found {len(objects)} objects in bucket '{container_name}'")
        return [{"name": obj.name, "size": obj.size} for obj in objects]
    except Exception as e:
        logger.error(f"Error listing files in bucket '{container_name}': {e}")
        return {"error": f"Listing failed - {e}"}
