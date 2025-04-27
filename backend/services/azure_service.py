from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from backend.config.settings import settings


def list_azure_vms():
    cls = get_driver(Provider.AZURE_ARM)
    driver = cls(
        tenant_id=settings.AZURE_TENANT_ID,
        subscription_id=settings.AZURE_SUBSCRIPTION_ID,
        key=settings.AZURE_CLIENT_ID,
        secret=settings.AZURE_SECRET
    )

    nodes = driver.list_nodes()
    return [{"name": node.name, "state": node.state} for node in nodes]
