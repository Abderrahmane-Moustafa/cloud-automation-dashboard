from fastapi import APIRouter
from backend.services.aws_service import list_aws_instances, create_aws_ec2, delete_aws_instance
from backend.services.azure_service import list_azure_vms, create_azure_vm, delete_azure_vm
from backend.models.vm import CreateAWSInstanceRequest, DeleteAWSInstanceRequest, CreateAzureVMRequest, DeleteAzureVMRequest

router = APIRouter(prefix="/api/vm", tags=["VM Operations"])

# Health check route
@router.get("/status")
def status():
    return {"status": "Cloud VM API is running"}

# List all AWS EC2 instances
@router.get("/aws")
def get_aws_instances():
    return {"aws_instances": list_aws_instances()}

# List all Azure VMs
@router.get("/azure")
def get_azure_vms():
    return {"azure_vms": list_azure_vms()}

# Create AWS EC2 VM Endpoint
@router.post("/aws/create")
def create_vm(request: CreateAWSInstanceRequest):
    # Pass the validated request fields to the EC2 creation function
    return create_aws_ec2(
        name=request.name,
        image_id=request.image_id,
        size_id=request.size_id,
        region=request.region
    )

# Delete AWS Instance Endpoint
@router.delete("/aws/delete")
def delete_vm_aws(request: DeleteAWSInstanceRequest):
    return delete_aws_instance(node_id=request.node_id, region=request.region)

# Create Azure VM Endpoint
@router.post("/azure/create")
def create_azure_vm_api(payload: CreateAzureVMRequest):
    return create_azure_vm(
        name=payload.name,
        image_id=payload.image_id,
        size_id=payload.size_id,
        location_id=payload.location_id
    )

# Delete Azure VM Endpoint
@router.delete("/azure/delete")
def delete_vm_azure(request: DeleteAzureVMRequest):
    return delete_azure_vm(node_id=request.node_id)

# Monitor status of all AWS EC2 instances with ping
@router.get("/aws/status")
def check_aws_instance_status():
    from backend.utils.ping_utils import ping_ip
    from backend.utils.logger import logger

    logger.info("Checking status and reachability of AWS instances...")
    instances = list_aws_instances()
    enhanced = []
    for inst in instances:
        public_ips = inst.get("public_ips", [])
        public_ip = public_ips[0] if public_ips else None

        is_up = ping_ip(public_ip)
        enhanced.append({
            "name": inst["name"],
            "state": inst["state"],
            "public_ip": public_ip,
            "ping_status": "reachable" if is_up else "unreachable"
        })
    return {"aws_status": enhanced}

# Monitor status of all Azure VMs with ping
@router.get("/azure/status")
def check_azure_vm_status():
    from backend.utils.ping_utils import ping_ip
    from backend.utils.logger import logger

    logger.info("Checking status and reachability of Azure VMs...")
    vms = list_azure_vms()
    enhanced = []
    for vm in vms:
        public_ip = vm.get("public_ips", [None])[0]
        is_up = ping_ip(public_ip)
        enhanced.append({
            "name": vm["name"],
            "state": vm["state"],
            "public_ip": public_ip,
            "ping_status": "reachable" if is_up else "unreachable"
        })
    return {"azure_status": enhanced}

# Monitoring Endpoint for AWS
@router.get("/aws/usage")
def aws_cpu_tracking(instance_id: str, region: str = "us-east-1"):
    from backend.services.aws_monitor import get_cpu_utilization
    from backend.utils.logger import logger

    logger.info(f"Fetching CPU usage for AWS instance: {instance_id}")
    usage = get_cpu_utilization(instance_id, region)
    return {
        "instance_id": instance_id,
        "cpu_utilization_percent": usage if usage is not None else "No data available"
    }

# Monitoring Endpoint for Azure
@router.get("/azure/usage")
def azure_cpu_tracking(resource_id: str):
    from backend.services.azure_monitor import get_azure_cpu_usage
    from backend.utils.logger import logger

    logger.info(f"Fetching Azure CPU usage for resource: {resource_id}")
    usage = get_azure_cpu_usage(resource_id)
    return {
        "resource_id": resource_id,
        "cpu_utilization_percent": usage if usage is not None else "No data available"
    }

