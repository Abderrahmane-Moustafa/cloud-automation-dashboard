from fastapi import APIRouter
from backend.services.aws_service import list_aws_instances
from backend.services.azure_service import list_azure_vms

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
