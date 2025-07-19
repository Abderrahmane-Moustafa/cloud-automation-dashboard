from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from backend.api import vm, storage, ui, metrics, billing

app = FastAPI(title="Cloud Resource Automation Dashboard")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(vm.router)
app.include_router(storage.router)
app.include_router(ui.router)
app.include_router(metrics.router)
app.include_router(billing.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Cloud Automation Dashboard!"}