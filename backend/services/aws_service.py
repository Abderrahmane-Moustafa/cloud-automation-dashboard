from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from backend.config.settings import settings


def list_aws_instances():
    cls = get_driver(Provider.EC2)
    driver = cls(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY, region="us-east-1")

    nodes = driver.list_nodes()
    return [{"name": node.name, "state": node.state} for node in nodes]
