from pydantic import BaseModel

class CreateAWSInstanceRequest(BaseModel):
    name: str
    image_id: str
    size_id: str
    region: str = "us-east-1"


class DeleteAWSInstanceRequest(BaseModel):
    node_id: str
    region: str = "us-east-1"


class CreateAzureVMRequest(BaseModel):
    name: str
    image_id: str
    size_id: str
    location_id: str = "brazilsouth"

