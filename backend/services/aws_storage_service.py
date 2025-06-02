from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver
from backend.config.settings import settings

# Upload file to AWS S3 bucket
def upload_file_to_s3(container_name: str, file_path: str, object_name: str):
    cls = get_driver(Provider.S3)
    driver = cls(settings.aws_access_key, settings.aws_secret_key)

    # Get container (S3 bucket) by name
    container = driver.get_container(container_name)

    # Upload file from local path to the container
    obj = driver.upload_object(
        file_path=file_path,
        container=container,
        object_name=object_name
    )

    # Return uploaded object details
    return {
        "object_name": obj.name,
        "size": obj.size,
        "url": obj.extra.get("object_uri", "N/A")
    }

# List files inside a specific S3 bucket
def list_files_in_s3(container_name: str):
    cls = get_driver(Provider.S3)
    driver = cls(settings.aws_access_key, settings.aws_secret_key)
    container = driver.get_container(container_name)

    # Return a list of object names and sizes
    return [{"name": obj.name, "size": obj.size} for obj in driver.list_container_objects(container)]