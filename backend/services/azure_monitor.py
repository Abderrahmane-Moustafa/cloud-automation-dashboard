from azure.identity import ClientSecretCredential
from azure.monitor.query import MetricsQueryClient, MetricAggregationType
from datetime import datetime, timedelta
from backend.config.settings import settings

# Retrieves average CPU usage for a specific Azure VM over the past 10 minutes
def get_azure_cpu_usage(resource_id: str):
    # Authenticate to Azure Monitor using your app credentials
    credential = ClientSecretCredential(
        tenant_id=settings.azure_tenant_id,
        client_id=settings.azure_client_id,
        client_secret=settings.azure_secret
    )

    # Initialize Azure Monitor Metrics client
    client = MetricsQueryClient(credential)

    # Define time window for the metric query (last 10 minutes)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=10)

    # Query Azure Monitor for "Percentage CPU" metric
    response = client.query_resource(
        resource_uri=resource_id,  # Full Azure Resource ID for the VM
        metric_names=["Percentage CPU"],  # Metric name
        timespan=(start_time, end_time),  # Time window
        aggregations=[MetricAggregationType.AVERAGE]  # Use average values
    )

    cpu_value = None  # Default if no data is returned

    # Traverse the returned metrics data
    for metric in response.metrics:
        for ts in metric.timeseries:
            for point in ts.data:
                if point.average is not None:
                    # Round and store the latest average value
                    cpu_value = round(point.average, 2)

    return cpu_value  # Return the CPU usage value (or None)
