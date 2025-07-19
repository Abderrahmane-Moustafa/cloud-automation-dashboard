from fastapi import APIRouter, Request

# Import Jinja2Templates to render HTML templates
from fastapi.templating import Jinja2Templates

# Import the function that gathers all dashboard data (VMs, storage, etc.)
from backend.services.dashboard_data import get_dashboard_data

# Create a new APIRouter instance for UI-related routes
router = APIRouter()

# Tell FastAPI where to find your HTML templates (e.g., dashboard.html)
templates = Jinja2Templates(directory="templates")

# Define the /dashboard route
@router.get("/dashboard")
def dashboard(request: Request):
    # Get all data needed to render the dashboard
    data = get_dashboard_data()

    # Render the dashboard.html template and pass the data to it
    return templates.TemplateResponse("dashboard.html", {
        "request": request,   # Required by FastAPI templates
        **data                # Unpack and inject all dashboard data into the HTML
    })
