from backend.services.aws_service import list_aws_instances
from backend.services.azure_service import list_azure_vms
from backend.services.aws_monitor import get_cpu_utilization
from backend.services.azure_monitor import get_azure_cpu_usage
from backend.services.aws_storage_service import list_files_in_s3
from backend.services.azure_storage_service import list_files_in_azure
from backend.utils.ping_utils import ping_ip


def get_dashboard_data():
    aws_vms = []
    azure_vms = []

    # Get and enrich AWS EC2 instances
    for vm in list_aws_instances():
        # Extract the first public IP (or None if not available)
        public_ip_list = vm.get("public_ips", [])
        public_ip = public_ip_list[0] if public_ip_list else None

        # Check if the public IP is reachable via ping
        ping = ping_ip(public_ip)

        # Get the instance ID (needed for CPU monitoring)
        instance_id = vm.get("id")

        # Retrieve average CPU usage via CloudWatch if ID is available
        cpu = get_cpu_utilization(instance_id, "us-east-1") if instance_id else None

        # Add enriched VM info to the list
        aws_vms.append({
            "name": vm["name"],
            "state": vm["state"],
            "public_ip": public_ip,
            "ping_status": "Reachable" if ping else "Unreachable",
            "cpu": cpu if cpu is not None else "-"
        })

    # Get and enrich Azure VMs
    for vm in list_azure_vms():
        # Extract the first public IP (or None)
        public_ip_list = vm.get("public_ips", [])
        public_ip = public_ip_list[0] if public_ip_list else None

        # Ping test for reachability
        ping = ping_ip(public_ip)

        # Get Azure resource ID (needed for Azure Monitor CPU usage)
        resource_id = vm.get("resource_id")

        # Retrieve average CPU usage via Azure Monitor
        cpu = get_azure_cpu_usage(resource_id) if resource_id else None

        # Add enriched VM info to the list
        azure_vms.append({
            "name": vm["name"],
            "state": vm["state"],
            "public_ip": public_ip,
            "ping_status": "Reachable" if ping else "Unreachable",
            "cpu": cpu if cpu is not None else "-"
        })

    # Define storage container names
    s3_container = "your-s3-bucket-name"
    azure_container = "your-azure-container-name"

    # Get file list from AWS S3
    try:
        aws_files = list_files_in_s3(s3_container)
    except:
        aws_files = []

    # Get file list from Azure Blob Storage
    try:
        azure_files = list_files_in_azure(azure_container)
    except:
        azure_files = []

    # Return everything as a dictionary to be passed to the dashboard template
    return {
        "aws_vms": aws_vms,
        "azure_vms": azure_vms,
        "aws_files": aws_files,
        "azure_files": azure_files
    }
