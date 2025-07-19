from fastapi import FastAPI
<<<<<<< HEAD
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
=======
from backend.api import vm, storage
from backend.ui import router as ui_router

app = FastAPI(title="Cloud Resource Automation Dashboard")

# Register all routers
app.include_router(vm.router)
app.include_router(storage.router)
app.include_router(ui_router)
>>>>>>> 91b5cf815370625b960aa9fdc3934c7152a49015

@app.get("/")
def read_root():
    return {"message": "Welcome to the Cloud Automation Dashboard!"}