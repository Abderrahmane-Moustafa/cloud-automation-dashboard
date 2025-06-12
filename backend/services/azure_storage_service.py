from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver
from backend.config.settings import settings
from backend.utils.logger import logger  # ← Logging

# Upload file to Azure Blob Storage
def upload_file_to_azure(container_name: str, file_path: str, object_name: str):
    logger.info(f"Uploading file to Azure Blob Storage: container={container_name}, object={object_name}")

    cls = get_driver(Provider.AZURE_BLOBS)
    driver = cls(settings.azure_storage_account, settings.azure_storage_key)

    try:
        container = driver.get_container(container_name)
    except Exception as e:
        logger.error(f"Failed to access Azure container '{container_name}': {e}")
        return {"error": f"Cannot access container '{container_name}' - {e}"}

    try:
        obj = driver.upload_object(
            file_path=file_path,
            container=container,
            object_name=object_name
        )

        logger.info(f"Uploaded file '{object_name}' to Azure container '{container_name}'")
        return {
            "object_name": obj.name,
            "size": obj.size,
            "url": obj.extra.get("object_uri", "N/A")
        }
    except Exception as e:
        logger.error(f"Failed to upload file '{object_name}' to Azure Blob: {e}")
        return {"error": f"Upload failed - {e}"}

# List files in a specific Azure Blob Storage container
def list_files_in_azure(container_name: str):
    logger.info(f"Listing files in Azure Blob container: {container_name}")

    cls = get_driver(Provider.AZURE_BLOBS)
    driver = cls(settings.azure_storage_account, settings.azure_storage_key)

    try:
        container = driver.get_container(container_name)
        objects = driver.list_container_objects(container)
        logger.info(f"Found {len(objects)} files in container '{container_name}'")
        return [{"name": obj.name, "size": obj.size} for obj in objects]
    except Exception as e:
        logger.error(f"Error listing files in Azure container '{container_name}': {e}")
        return {"error": f"Listing failed - {e}"}
