from fastapi import FastAPI
from backend.api import vm, storage
from backend.ui import router as ui_router

app = FastAPI(title="Cloud Resource Automation Dashboard")

# Register all routers
app.include_router(vm.router)
app.include_router(storage.router)
app.include_router(ui_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Cloud Automation Dashboard!"}
