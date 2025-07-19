from fastapi import APIRouter, Query
from backend.services.aws_billing_service import get_aws_total_cost, get_aws_billing_summary
from backend.services.azure_billing_service import get_azure_total_cost, get_azure_billing_summary

router = APIRouter(prefix="/api/billing", tags=["Billing"])

@router.get("/aws")
def fetch_aws_billing():
    return get_aws_total_cost()

@router.get("/azure")
def fetch_azure_billing():
    return get_azure_total_cost()

@router.get("/aws/summary")
def fetch_aws_billing_summary(months: int = Query(default=6, description="Number of past months")):
    return get_aws_billing_summary(months_back=months)

@router.get("/azure/summary")
def fetch_azure_billing_summary(months: int = Query(default=6, description="Number of past months")):
    return get_azure_billing_summary(months_back=months)
