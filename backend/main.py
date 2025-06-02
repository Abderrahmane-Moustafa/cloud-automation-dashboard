from fastapi import FastAPI
from backend.api import vm, storage  # ← add this

app = FastAPI(title="Cloud Resource Automation Dashboard")

app.include_router(vm.router)
app.include_router(storage.router)  # ← add this

@app.get("/")
def read_root():
    return {"message": "Welcome to the Cloud Automation Dashboard!"}
