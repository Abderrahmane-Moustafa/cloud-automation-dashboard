from fastapi import APIRouter
from backend.services.aws_service import list_aws_instances, create_aws_ec2
from backend.services.azure_service import list_azure_vms
from backend.models.vm import CreateAWSInstanceRequest


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
    return create_aws_ec2(
        name=request.name,
        image_id=request.image_id,
        size_id=request.size_id,
        region=request.region
    )