import boto3
from datetime import datetime, timedelta
from backend.config.settings import settings

# Fetches the average CPU utilization for an AWS EC2 instance using CloudWatch
def get_cpu_utilization(instance_id: str, region: str = "us-east-1"):
    # Create a CloudWatch client with your AWS credentials and region
    client = boto3.client(
        'cloudwatch',
        aws_access_key_id=settings.aws_access_key,
        aws_secret_access_key=settings.aws_secret_key,
        region_name=region
    )

    # Define the time window for the metric query (last 10 minutes)
    now = datetime.utcnow()

    # Request CPU utilization metrics from CloudWatch
    response = client.get_metric_statistics(
        Namespace='AWS/EC2',                 # Metric namespace for EC2
        MetricName='CPUUtilization',         # Metric to query
        Dimensions=[
            {'Name': 'InstanceId', 'Value': instance_id}  # Filter by instance ID
        ],
        StartTime=now - timedelta(minutes=10),  # Start of time range
        EndTime=now,                             # End of time range (now)
        Period=300,                              # Period (5 minutes in seconds)
        Statistics=['Average']                   # Return average CPU usage
    )

    # Extract CPU values from the returned datapoints
    datapoints = response.get('Datapoints', [])
    if datapoints:
        # Return the last average value, rounded to 2 decimals
        return round(datapoints[-1]['Average'], 2)
    return None  # If no data, return None
