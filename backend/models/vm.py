from pydantic import BaseModel

class CreateAWSInstanceRequest(BaseModel):
    name: str
    image_id: str
    size_id: str
    region: str = "us-east-1"
