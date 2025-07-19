import requests
from azure.identity import ClientSecretCredential
from backend.config.settings import settings
from datetime import datetime, timedelta


def get_azure_total_cost():
    try:
        credential = ClientSecretCredential(
            tenant_id=settings.azure_tenant_id,
            client_id=settings.azure_client_id,
            client_secret=settings.azure_secret
        )

        token = credential.get_token("https://management.azure.com/.default").token

        headers = {
            "Authorization": f"Bearer {token}"
        }

        today = datetime.utcnow().date()
        start = today.replace(day=1).isoformat()
        end = today.isoformat()

        url = (
            f"https://management.azure.com/subscriptions/{settings.azure_subscription_id}/providers/Microsoft.CostManagement/query?api-version=2023-03-01"
        )

        body = {
            "type": "ActualCost",
            "timeframe": "Custom",
            "timePeriod": {
                "from": start,
                "to": end
            },
            "dataset": {
                "granularity": "None",
                "aggregation": {
                    "totalCost": {
                        "name": "PreTaxCost",
                        "function": "Sum"
                    }
                },
                "grouping": []
            }
        }

        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()

        total_cost = data['properties']['rows'][0][0]
        return {
            "month": start,
            "currency": "USD",
            "totalCost": round(float(total_cost), 2)
        }

    except Exception as e:
        return {"error": f"Failed to fetch Azure billing: {e}"}


def get_azure_billing_summary(months_back: int = 6):
    try:
        credential = ClientSecretCredential(
            tenant_id=settings.azure_tenant_id,
            client_id=settings.azure_client_id,
            client_secret=settings.azure_secret
        )

        token = credential.get_token("https://management.azure.com/.default").token

        headers = {
            "Authorization": f"Bearer {token}"
        }

        today = datetime.utcnow().date()
        first_day_of_current_month = today.replace(day=1)
        start = (first_day_of_current_month - timedelta(days=30 * months_back)).replace(day=1).isoformat()
        end = today.isoformat()

        url = (
            f"https://management.azure.com/subscriptions/{settings.azure_subscription_id}/providers/Microsoft.CostManagement/query?api-version=2023-03-01"
        )

        body = {
            "type": "ActualCost",
            "timeframe": "Custom",
            "timePeriod": {
                "from": start,
                "to": end
            },
            "dataset": {
                "granularity": "Monthly",
                "aggregation": {
                    "totalCost": {
                        "name": "PreTaxCost",
                        "function": "Sum"
                    }
                },
                "grouping": []
            }
        }

        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()

        total = 0.0
        for row in data['properties']['rows']:
            total += float(row[0])

        return {
            "start": start,
            "end": end,
            "currency": "USD",
            "totalCost": round(total, 2)
        }

    except Exception as e:
        return {"error": f"Failed to fetch Azure billing summary: {e}"}
