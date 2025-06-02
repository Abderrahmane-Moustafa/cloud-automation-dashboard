from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver
from backend.config.settings import settings

# Upload file to Azure Blob Storage
def upload_file_to_azure(container_name: str, file_path: str, object_name: str):
    cls = get_driver(Provider.AZURE_BLOBS)
    driver = cls(settings.azure_storage_account, settings.azure_storage_key)

    container = driver.get_container(container_name)

    obj = driver.upload_object(
        file_path=file_path,
        container=container,
        object_name=object_name
    )

    return {
        "object_name": obj.name,
        "size": obj.size,
        "url": obj.extra.get("object_uri", "N/A")
    }

# List files in a specific Azure Blob Storage container
def list_files_in_azure(container_name: str):
    cls = get_driver(Provider.AZURE_BLOBS)
    driver = cls(settings.azure_storage_account, settings.azure_storage_key)

    container = driver.get_container(container_name)
    return [{"name": obj.name, "size": obj.size} for obj in driver.list_container_objects(container)]
