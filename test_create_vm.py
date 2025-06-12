from backend.services.azure_service import create_azure_vm

result = create_azure_vm(
    name="test-vm-1",
    image_id="Canonical:0001-com-ubuntu-server-jammy:24_04-lts:gen2",
    size_id="Standard_B1ls",
    location_id="eastus"
)

print(result)
