from pydantic import BaseModel

# This Pydantic model defines the structure and validation
# for the JSON body expected when creating a new AWS EC2 instance.
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

class DeleteAzureVMRequest(BaseModel):
    node_id: str


