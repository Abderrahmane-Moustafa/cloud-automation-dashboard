from fastapi import FastAPI
from backend.api import vm, storage, ui

app = FastAPI(title="Cloud Resource Automation Dashboard")

app.include_router(vm.router)
app.include_router(storage.router)
app.include_router(ui.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Cloud Automation Dashboard!"}
