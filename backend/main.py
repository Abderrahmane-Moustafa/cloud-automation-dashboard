from fastapi import FastAPI
from backend.api import vm

app = FastAPI(title="Cloud Resource Automation Dashboard")

# Include API routers
app.include_router(vm.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Cloud Automation Dashboard!"}
