from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from backend.services.aws_service import create_aws_ec2, list_aws_instances
from backend.services.azure_service import create_azure_vm, list_azure_vms
from backend.services.aws_storage_service import upload_file_to_s3
from backend.services.azure_storage_service import upload_file_to_azure
from backend.services.aws_monitor import get_cpu_utilization
from backend.services.azure_monitor import get_azure_cpu_usage
from backend.utils.ping_utils import ping_ip

import os
import tempfile
import shutil

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
def show_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@router.post("/dashboard/aws-vm")
def create_aws_vm(request: Request, name: str = Form(...), image_id: str = Form(...), size_id: str = Form(...), region: str = Form(...)):
    result = create_aws_ec2(name, image_id, size_id, region)
    return templates.TemplateResponse("dashboard.html", {"request": request, "aws_vm_result": result})

@router.post("/dashboard/azure-vm")
def create_azure_vm_view(request: Request, name: str = Form(...), image_id: str = Form(...), size_id: str = Form(...), location_id: str = Form(...)):
    result = create_azure_vm(name, image_id, size_id, location_id)
    return templates.TemplateResponse("dashboard.html", {"request": request, "azure_vm_result": result})

@router.post("/dashboard/aws-upload")
def upload_to_aws(request: Request, file: UploadFile = File(...), container_name: str = Form(...), object_name: str = Form(...)):
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, file.filename)
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    result = upload_file_to_s3(container_name, temp_path, object_name)
    os.remove(temp_path)
    return templates.TemplateResponse("dashboard.html", {"request": request, "aws_upload_result": result})

@router.post("/dashboard/azure-upload")
def upload_to_azure(request: Request, file: UploadFile = File(...), container_name: str = Form(...), object_name: str = Form(...)):
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, file.filename)
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    result = upload_file_to_azure(container_name, temp_path, object_name)
    os.remove(temp_path)
    return templates.TemplateResponse("dashboard.html", {"request": request, "azure_upload_result": result})

@router.get("/dashboard/status", response_class=HTMLResponse)
def check_all_status(request: Request):
    aws_status = []
    aws_nodes = list_aws_instances()
    for inst in aws_nodes:
        ip = inst["public_ips"][0] if inst["public_ips"] else "N/A"
        status = "reachable" if ip != "N/A" and ping_ip(ip) else "unreachable"
        instance_id = inst.get("id")  # Use actual instance ID
        usage = get_cpu_utilization(instance_id) if instance_id else "No ID"
        aws_status.append({
            "name": inst["name"],
            "ip": ip,
            "ping": status,
            "cpu": usage or "No Data"
        })

    azure_status = []
    for vm in list_azure_vms():
        ip = vm["public_ips"][0] if vm["public_ips"] else "N/A"
        status = "reachable" if ip != "N/A" and ping_ip(ip) else "unreachable"
        usage = get_azure_cpu_usage(vm["name"]) or "No Data"
        azure_status.append({
            "name": vm["name"],
            "ip": ip,
            "ping": status,
            "cpu": usage
        })

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "aws_status": aws_status,
        "azure_status": azure_status
    })
