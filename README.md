# Cloud Resource Automation Dashboard

This project is a web application that helps manage cloud resources on AWS and 
Azure. It is built using FastAPI as the backend framework and Apache Libcloud to 
interact with cloud providers. 

## Features

- List AWS EC2 instances
- List Azure Virtual Machines
- Environment variable management using a .env file
- API documentation available through Swagger UI

## Technologies Used

- Python 3.12
- FastAPI
- Apache Libcloud
- Uvicorn
- Pydantic Settings

## Project Structure

- cloud_resource_dashboard/
  - backend/
    - api/
      - vm.py
    - config/
      - settings.py
    - services/
      - aws_service.py
      - azure_service.py
    - main.py
  - .env (not included in the repository)
  - .gitignore
  - requirements.txt
  - README.md

## How to Run the Project

1. Clone the repository:
