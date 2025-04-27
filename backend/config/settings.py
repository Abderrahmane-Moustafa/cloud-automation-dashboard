from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AZURE_SUBSCRIPTION_ID: str
    AZURE_TENANT_ID: str
    AZURE_CLIENT_ID: str
    AZURE_SECRET: str

    class Config:
        env_file = ".env"

settings = Settings()
