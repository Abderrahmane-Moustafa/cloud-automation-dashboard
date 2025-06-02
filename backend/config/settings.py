from pydantic_settings import BaseSettings
from pydantic import BaseModel

class Settings(BaseSettings):
    aws_access_key: str
    aws_secret_key: str
    azure_subscription_id: str
    azure_tenant_id: str
    azure_client_id: str
    azure_secret: str

    # Azure Blob Storage credentials
    azure_storage_account: str
    azure_storage_key: str

    class Config:
        env_file = ".env"

settings = Settings()

class VMCreateRequest(BaseModel):
    name: str
    image_id: str
    size_id: str
    region: str
