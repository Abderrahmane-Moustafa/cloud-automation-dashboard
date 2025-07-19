from fastapi import APIRouter, Response
from backend.utils.metrics import get_metrics, track_api_request, track_vm_operation, track_storage_operation

router = APIRouter(prefix="/api/metrics", tags=["Metrics"])

@router.get("/prometheus")
async def prometheus_metrics():
    """
    Prometheus metrics endpoint for Grafana scraping
    Usage: http://localhost:8000/api/metrics/prometheus
    """
    return await get_metrics()

@router.get("/health")
async def health_check():
    """Simple health check for monitoring"""
    return {
        "status": "healthy",
        "service": "cloud-dashboard",
        "metrics_endpoint": "/api/metrics/prometheus"
    }