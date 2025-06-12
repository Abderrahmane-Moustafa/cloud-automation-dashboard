from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from backend.config.settings import settings
from backend.utils.logger import logger  # ← Logging added


# List all AWS EC2 instances in the configured region
def list_aws_instances():
    cls = get_driver(Provider.EC2)
    driver = cls(settings.aws_access_key, settings.aws_secret_key, region="us-east-1")

    nodes = driver.list_nodes()
    logger.info(f"Listed {len(nodes)} AWS EC2 instances.")

    # Return basic info about each AWS EC2 node
    return [{
        "name": node.name,
        "state": node.state,
        "public_ips": node.public_ips,
        "private_ips": node.private_ips
    } for node in nodes]


# Create an AWS EC2 Instance
def create_aws_ec2(name, image_id, size_id, region="us-east-1"):
    logger.info(
        f"Request to create AWS EC2 instance: name={name}, image_id={image_id}, size_id={size_id}, region={region}")

    # Get the EC2 driver class from Apache Libcloud
    cls = get_driver(Provider.EC2)

    # Initialize the driver using AWS credentials and target region
    driver = cls(settings.aws_access_key, settings.aws_secret_key, region=region)

    # Retrieve the list of available instance sizes and images
    sizes = driver.list_sizes()
    images = driver.list_images()

    # Filter the size and image by the provided IDs
    size = [s for s in sizes if s.id == size_id][0]
    image = [i for i in images if i.id == image_id][0]

    # Handle the case where either size or image is not found
    if not size or not image:
        logger.error(f"Size or image not found for AWS EC2 creation.")
        return {"error": "Size or image not found"}

    try:
        # Create a new EC2 instance with the specified parameters
        node = driver.create_node(name=name, image=image, size=size)
        logger.info(f"AWS EC2 instance created: id={node.id}, name={node.name}, state={node.state}")

        # Return essential instance details to the API caller
        return {
            "id": node.id,
            "name": node.name,
            "state": node.state,
            "public_ips": node.public_ips,
            "private_ips": node.private_ips
        }
    except Exception as e:
        logger.error(f"Failed to create AWS EC2 instance: {e}")
        return {"error": f"Instance creation failed - {e}"}


# Delete an AWS EC2 instance by node ID
def delete_aws_instance(node_id: str, region="us-east-1"):
    logger.info(f"Request to delete AWS EC2 instance: node_id={node_id}, region={region}")

    cls = get_driver(Provider.EC2)
    driver = cls(settings.aws_access_key, settings.aws_secret_key, region=region)

    # Find the instance to delete by its ID
    node = next((n for n in driver.list_nodes() if n.id == node_id), None)

    if not node:
        logger.warning(f"AWS EC2 instance with ID '{node_id}' not found for deletion.")
        return {"error": f"Instance with ID {node_id} not found."}

    try:
        result = driver.destroy_node(node)
        logger.info(f"AWS EC2 instance deleted: id={node_id}, result={result}")
        return {"deleted": result, "node_id": node_id}
    except Exception as e:
        logger.error(f"Failed to delete AWS EC2 instance '{node_id}': {e}")
        return {"error": f"Deletion failed - {e}"}
