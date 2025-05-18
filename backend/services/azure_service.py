from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.compute.base import NodeAuthSSHKey
from backend.config.settings import settings


def list_azure_vms():
    cls = get_driver(Provider.AZURE_ARM)
    driver = cls(
        tenant_id=settings.azure_tenant_id,
        subscription_id=settings.azure_subscription_id,
        key=settings.azure_client_id,
        secret=settings.azure_secret
    )

    nodes = driver.list_nodes()
    return [{"name": node.name, "state": node.state} for node in nodes]


# Function to create an Azure VM
def create_azure_vm(name, image_id, size_id, location_id="brazilsouth"):
    cls = get_driver(Provider.AZURE_ARM)
    driver = cls(
        tenant_id=settings.azure_tenant_id,
        subscription_id=settings.azure_subscription_id,
        key=settings.azure_client_id,
        secret=settings.azure_secret
    )

    # Get location object
    locations = driver.list_locations()
    location = next((l for l in locations if l.id == location_id), None)
    if not location:
        return {"error": f"Location '{location_id}' not found"}

    # Get size object
    sizes = driver.list_sizes(location=location)
    size = next((s for s in sizes if s.id == size_id), None)
    if not size:
        return {"error": f"Size '{size_id}' not found in location '{location_id}'"}

    # Get image object
    try:
        image = driver.get_image(image_id=image_id, location=location)
    except Exception as e:
        return {"error": f"Image '{image_id}' invalid: {e}"}

    # Define SSH public key
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDkGXkEokkmoOdVVl5YoJyTeyE5O/kwEjAS3Y7/Vt7gNvL1DsEnV0aDToXBMoaAk35TiOswzF+T4wv68Kra2pPNazPQoCvd2CtMr3TXByvMe16pC6ccrWjksA8AhLL/opmDjPyaDgeF+1qsp1vz0t3LlGLjUyIdnyCYCfBDdEH4UZwlk8Vm/uK8dipkRDGyGjy6UdUyv8eFhrrB/8jxfrxmsoqG4pW3g5PNyxi8p6Ft95YKCOFbApsHnFdYqd3maDD9QRo5P3GKbGOlGwGyU9xzjOiQinmTcQJc0nQf/BqupEqg3qWNXDM7o76HX/WASg8GSvRxInzHMR545Aglyxnb azureuser"
    auth = NodeAuthSSHKey(public_key)

    # Create VM
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

    return {
        "id": node.id,
        "name": node.name,
        "state": node.state,
        "public_ips": node.public_ips,
        "private_ips": node.private_ips
    }


# Delete an Azure VM Function
def delete_azure_vm(node_id: str):
    cls = get_driver(Provider.AZURE_ARM)
    driver = cls(
        tenant_id=settings.azure_tenant_id,
        subscription_id=settings.azure_subscription_id,
        key=settings.azure_client_id,
        secret=settings.azure_secret
    )

    print("Listing Azure VMs visible to Libcloud:")
    for n in driver.list_nodes():
        print(f"• {n.name} --> {n.id}")

    node = next((n for n in driver.list_nodes() if n.id == node_id), None)

    if not node:
        print("Node not found for deletion.")
        return {"error": f"Instance with ID '{node_id}' not found."}

    try:
        print(f"Attempting to delete node: {node.id}")
        result = driver.destroy_node(
            node,
            ex_destroy_nic=True,
            ex_destroy_vhd=True,
            ex_poll_qty=10,
            ex_poll_wait=10
        )
        print(f"Deletion result: {result}")
        return {"deleted": result, "node_id": node_id}
    except Exception as e:
        print(f"Exception during deletion: {e}")
        return {"error": f"Failed to delete node: {str(e)}"}
