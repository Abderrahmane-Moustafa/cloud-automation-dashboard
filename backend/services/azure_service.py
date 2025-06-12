from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.compute.base import NodeAuthSSHKey
from backend.config.settings import settings
from backend.utils.logger import logger  # ← Logging

# List all Azure VMs available in the subscription
def list_azure_vms():
    cls = get_driver(Provider.AZURE_ARM)
    driver = cls(
        tenant_id=settings.azure_tenant_id,
        subscription_id=settings.azure_subscription_id,
        key=settings.azure_client_id,
        secret=settings.azure_secret
    )

    nodes = driver.list_nodes()
    for node in nodes:
        print(f"• {node.name} --> {node.id}")

    logger.info(f"Listed {len(nodes)} Azure VMs.")
    return [{
        "name": node.name,
        "state": node.state,
        "public_ips": node.public_ips,
        "private_ips": node.private_ips
    } for node in nodes]


# Function to create an Azure VM
def create_azure_vm(name, image_id, size_id, location_id="brazilsouth"):
    # Get the Azure ARM driver class
    cls = get_driver(Provider.AZURE_ARM)

    # Initialize the driver using credentials from .env
    driver = cls(
        tenant_id=settings.azure_tenant_id,
        subscription_id=settings.azure_subscription_id,
        key=settings.azure_client_id,
        secret=settings.azure_secret
    )

    logger.info(f"Request to create Azure VM: name={name}, image_id={image_id}, size_id={size_id}, location_id={location_id}")

    # Get the location object that matches the provided location_id
    locations = driver.list_locations()
    location = next((l for l in locations if l.id == location_id), None)
    if not location:
        logger.error(f"Location '{location_id}' not found.")
        return {"error": f"Location '{location_id}' not found"}

    # Get the VM size object that matches the provided size_id
    sizes = driver.list_sizes(location=location)
    size = next((s for s in sizes if s.id == size_id), None)
    if not size:
        logger.error(f"Size '{size_id}' not found in location '{location_id}'.")
        return {"error": f"Size '{size_id}' not found in location '{location_id}'"}

    # Get the image object (OS) by image_id and region
    try:
        image = driver.get_image(image_id=image_id, location=location)
    except Exception as e:
        logger.error(f"Image '{image_id}' invalid: {e}")
        return {"error": f"Image '{image_id}' invalid: {e}"}

    # Define the public SSH key to be used for authentication to the VM
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDkGXkEokkmoOdVVl5YoJyTeyE5O/kwEjAS3Y7/Vt7gNvL1DsEnV0aDToXBMoaAk35TiOswzF+T4wv68Kra2pPNazPQoCvd2CtMr3TXByvMe16pC6ccrWjksA8AhLL/opmDjPyaDgeF+1qsp1vz0t3LlGLjUyIdnyCYCfBDdEH4UZwlk8Vm/uK8dipkRDGyGjy6UdUyv8eFhrrB/8jxfrxmsoqG4pW3g5PNyxi8p6Ft95YKCOFbApsHnFdYqd3maDD9QRo5P3GKbGOlGwGyU9xzjOiQinmTcQJc0nQf/BqupEqg3qWNXDM7o76HX/WASg8GSvRxInzHMR545Aglyxnb azureuser"
    auth = NodeAuthSSHKey(public_key)

    # Create the virtual machine with all required parameters
    node = driver.create_node(
        name=name,
        image=image,
        size=size,
        location=location,
        auth=auth,
        ex_resource_group="TH-Machine_group",
        ex_network="TH-Machine-vnet",
        ex_subnet="default",
        ex_use_managed_disks=True
    )

    logger.info(f"Azure VM created successfully: id={node.id}, name={node.name}, state={node.state}")

    # Return relevant VM info for the dashboard or API user
    return {
        "id": node.id,
        "name": node.name,
        "state": node.state,
        "public_ips": node.public_ips,
        "private_ips": node.private_ips
    }


# Delete an Azure VM Function
def delete_azure_vm(node_id: str):
    # Get the Azure ARM driver
    cls = get_driver(Provider.AZURE_ARM)

    # Initialize the driver with credentials from the environment
    driver = cls(
        tenant_id=settings.azure_tenant_id,
        subscription_id=settings.azure_subscription_id,
        key=settings.azure_client_id,
        secret=settings.azure_secret
    )

    # Print available VMs to verify what's visible from the current credentials
    print("Listing Azure VMs visible to Libcloud:")
    for n in driver.list_nodes():
        print(f"\u2022 {n.name} --> {n.id}")

    # Find the VM node by matching the given node_id
    node = next((n for n in driver.list_nodes() if n.id == node_id), None)

    # If no matching node is found, return an error message
    if not node:
        logger.warning(f"Azure VM with ID '{node_id}' not found for deletion.")
        print("Node not found for deletion.")
        return {"error": f"Instance with ID '{node_id}' not found."}

    try:
        # Attempt to delete the node and clean up associated resources
        logger.info(f"Attempting to delete Azure VM: id={node.id}, name={node.name}")
        result = driver.destroy_node(
            node,
            ex_destroy_nic=True,
            ex_destroy_vhd=True,
            ex_poll_qty=10,
            ex_poll_wait=10
        )
        logger.info(f"Deletion result for Azure VM '{node_id}': {result}")
        return {"deleted": result, "node_id": node_id}
    except Exception as e:
        logger.error(f"Failed to delete Azure VM '{node_id}': {e}")
        return {"error": f"Failed to delete node: {str(e)}"}
