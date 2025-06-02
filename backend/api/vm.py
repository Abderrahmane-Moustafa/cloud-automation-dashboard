from fastapi import APIRouter
from backend.services.aws_service import list_aws_instances, create_aws_ec2, delete_aws_instance
from backend.services.azure_service import list_azure_vms, create_azure_vm, delete_azure_vm
from backend.models.vm import CreateAWSInstanceRequest, DeleteAWSInstanceRequest, CreateAzureVMRequest, DeleteAzureVMRequest


router = APIRouter(prefix="/api/vm", tags=["VM Operations"])

@router.get("/status")
def status():
    return {"status": "Cloud VM API is running"}

@router.get("/aws")
def get_aws_instances():
    return {"aws_instances": list_aws_instances()}

@router.get("/azure")
def get_azure_vms():
    return {"azure_vms": list_azure_vms()}

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

# Create VM Azure Endpoint
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
