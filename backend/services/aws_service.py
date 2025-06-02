from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from backend.config.settings import settings


def list_aws_instances():
    cls = get_driver(Provider.EC2)
    driver = cls(settings.aws_access_key, settings.aws_secret_key, region="us-east-1")
    nodes = driver.list_nodes()
    return [{"name": node.name, "state": node.state} for node in nodes]

# Create an AWS Instance
def create_aws_ec2(name, image_id, size_id, region="us-east-1"):
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
        return {"error": "Size or image not found"}

    # Create a new EC2 instance with the specified parameters
    node = driver.create_node(name=name, image=image, size=size)

    # Return essential instance details to the API caller
    return {
        "id": node.id,
        "name": node.name,
        "state": node.state,
        "public_ips": node.public_ips,
        "private_ips": node.private_ips
    }


# Delete an AWS instance
def delete_aws_instance(node_id: str, region="us-east-1"):
    cls = get_driver(Provider.EC2)
    driver = cls(settings.aws_access_key, settings.aws_secret_key, region="us-east-1")
    # Find the instance to delete by its ID
    node = next((n for n in driver.list_nodes() if n.id == node_id), None)

    if not node:
        return {"error": f"Instance with ID {node_id} not found."}

    result = driver.destroy_node(node)
    return {"deleted": result, "node_id": node_id}