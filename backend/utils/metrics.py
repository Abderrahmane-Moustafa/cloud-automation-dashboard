# metrics.py - Prometheus metrics for Grafana
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
import time
from typing import Dict, List
from backend.services.aws_service import list_aws_instances
from backend.services.azure_service import list_azure_vms
from backend.services.aws_monitor import get_cpu_utilization
from backend.services.azure_monitor import get_azure_cpu_usage
from backend.utils.ping_utils import ping_ip
from backend.utils.logger import logger

# Define Prometheus metrics
# Counters (always increasing)
api_requests_total = Counter(
    'cloud_dashboard_api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

vm_operations_total = Counter(
    'cloud_dashboard_vm_operations_total',
    'Total VM operations',
    ['provider', 'operation', 'status']
)

storage_operations_total = Counter(
    'cloud_dashboard_storage_operations_total',
    'Total storage operations',
    ['provider', 'operation', 'status']
)

# Gauges (can go up and down)
vm_count = Gauge(
    'cloud_dashboard_vm_count',
    'Number of VMs per provider',
    ['provider', 'state']
)

vm_cpu_usage = Gauge(
    'cloud_dashboard_vm_cpu_usage_percent',
    'CPU usage percentage per VM',
    ['provider', 'vm_name', 'vm_id']
)

vm_reachability = Gauge(
    'cloud_dashboard_vm_reachable',
    'VM reachability status (1=reachable, 0=unreachable)',
    ['provider', 'vm_name', 'public_ip']
)

storage_upload_size = Histogram(
    'cloud_dashboard_storage_upload_size_bytes',
    'Size of uploaded files',
    ['provider']
)

# System metrics
system_health = Gauge(
    'cloud_dashboard_system_health',
    'Overall system health score (0-100)',
    []
)


class MetricsCollector:
    """
    Collects metrics from AWS and Azure for Prometheus/Grafana
    """

    def __init__(self):
        self.last_collection = 0
        self.collection_interval = 60  # seconds

    async def collect_all_metrics(self):
        """
        Collect all metrics from both cloud providers
        """
        current_time = time.time()

        # Only collect if enough time has passed (rate limiting)
        if current_time - self.last_collection < self.collection_interval:
            return

        logger.info("Collecting metrics for Prometheus/Grafana...")

        try:
            # Collect AWS metrics
            await self._collect_aws_metrics()

            # Collect Azure metrics
            await self._collect_azure_metrics()

            # Calculate system health
            self._calculate_system_health()

            self.last_collection = current_time
            logger.info("Metrics collection completed successfully")

        except Exception as e:
            logger.error(f"Error during metrics collection: {e}")

    async def _collect_aws_metrics(self):
        """Collect AWS-specific metrics"""
        try:
            aws_instances = list_aws_instances()

            # Count VMs by state
            state_counts = {}
            reachable_count = 0
            total_cpu = 0
            cpu_count = 0

            for instance in aws_instances:
                state = instance.get("state", "unknown")
                state_counts[state] = state_counts.get(state, 0) + 1

                # Check reachability
                public_ip = instance["public_ips"][0] if instance["public_ips"] else None
                is_reachable = ping_ip(public_ip) if public_ip else False

                vm_reachability.labels(
                    provider="aws",
                    vm_name=instance["name"],
                    public_ip=public_ip or "none"
                ).set(1 if is_reachable else 0)

                if is_reachable:
                    reachable_count += 1

                # Get CPU usage
                if instance.get("id"):
                    try:
                        cpu_usage = get_cpu_utilization(instance["id"])
                        if cpu_usage is not None:
                            vm_cpu_usage.labels(
                                provider="aws",
                                vm_name=instance["name"],
                                vm_id=instance["id"]
                            ).set(cpu_usage)
                            total_cpu += cpu_usage
                            cpu_count += 1
                    except Exception as e:
                        logger.warning(f"Could not get CPU for AWS instance {instance['name']}: {e}")

            # Set state counts
            for state, count in state_counts.items():
                vm_count.labels(provider="aws", state=state).set(count)

            logger.info(f"AWS metrics: {len(aws_instances)} instances, {reachable_count} reachable")

        except Exception as e:
            logger.error(f"Error collecting AWS metrics: {e}")

    async def _collect_azure_metrics(self):
        """Collect Azure-specific metrics"""
        try:
            azure_vms = list_azure_vms()

            # Count VMs by state
            state_counts = {}
            reachable_count = 0
            total_cpu = 0
            cpu_count = 0

            for vm in azure_vms:
                state = vm.get("state", "unknown")
                state_counts[state] = state_counts.get(state, 0) + 1

                # Check reachability
                public_ip = vm["public_ips"][0] if vm["public_ips"] else None
                is_reachable = ping_ip(public_ip) if public_ip else False

                vm_reachability.labels(
                    provider="azure",
                    vm_name=vm["name"],
                    public_ip=public_ip or "none"
                ).set(1 if is_reachable else 0)

                if is_reachable:
                    reachable_count += 1

                # Get CPU usage (you may need to fix the resource ID format)
                try:
                    cpu_usage = get_azure_cpu_usage(vm["name"])  # This might need fixing
                    if cpu_usage is not None:
                        vm_cpu_usage.labels(
                            provider="azure",
                            vm_name=vm["name"],
                            vm_id=vm["name"]  # Using name as ID for Azure
                        ).set(cpu_usage)
                        total_cpu += cpu_usage
                        cpu_count += 1
                except Exception as e:
                    logger.warning(f"Could not get CPU for Azure VM {vm['name']}: {e}")

            # Set state counts
            for state, count in state_counts.items():
                vm_count.labels(provider="azure", state=state).set(count)

            logger.info(f"Azure metrics: {len(azure_vms)} VMs, {reachable_count} reachable")

        except Exception as e:
            logger.error(f"Error collecting Azure metrics: {e}")

    def _calculate_system_health(self):
        """Calculate overall system health score"""
        try:
            # Simple health calculation based on:
            # - Number of reachable VMs
            # - Average CPU usage
            # - Any recent errors

            # This is a basic implementation - you can make it more sophisticated
            health_score = 100  # Start with perfect health

            # You can add more sophisticated health calculations here
            # For now, just set a basic score
            system_health.set(health_score)

        except Exception as e:
            logger.error(f"Error calculating system health: {e}")
            system_health.set(0)


# Global metrics collector instance
metrics_collector = MetricsCollector()


# Middleware functions for tracking API requests
def track_api_request(method: str, endpoint: str, status_code: int):
    """Track API request metrics"""
    api_requests_total.labels(
        method=method,
        endpoint=endpoint,
        status=str(status_code)
    ).inc()


def track_vm_operation(provider: str, operation: str, success: bool):
    """Track VM operation metrics"""
    status = "success" if success else "error"
    vm_operations_total.labels(
        provider=provider,
        operation=operation,
        status=status
    ).inc()


def track_storage_operation(provider: str, operation: str, success: bool, file_size: int = None):
    """Track storage operation metrics"""
    status = "success" if success else "error"
    storage_operations_total.labels(
        provider=provider,
        operation=operation,
        status=status
    ).inc()

    if file_size and success:
        storage_upload_size.labels(provider=provider).observe(file_size)


async def get_metrics() -> Response:
    """
    Endpoint that returns Prometheus metrics for Grafana to scrape
    """
    # Collect fresh metrics
    await metrics_collector.collect_all_metrics()

    # Return metrics in Prometheus format
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )