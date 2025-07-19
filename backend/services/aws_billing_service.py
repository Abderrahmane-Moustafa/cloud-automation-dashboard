from datetime import datetime, timedelta
import boto3
from backend.config.settings import settings

def get_aws_total_cost():
    client = boto3.client(
        "ce",
        aws_access_key_id=settings.aws_access_key,
        aws_secret_access_key=settings.aws_secret_key,
        region_name="us-east-1"
    )

    today = datetime.utcnow().date()
    start = today.replace(day=1).isoformat()
    end = today.isoformat()

    response = client.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"]
    )

    amount = response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"]
    return {
        "month": start,
        "currency": "USD",
        "totalCost": round(float(amount), 2)
    }

def get_aws_billing_summary(months_back: int = 6):
    client = boto3.client(
        "ce",
        aws_access_key_id=settings.aws_access_key,
        aws_secret_access_key=settings.aws_secret_key,
        region_name="us-east-1"
    )

    today = datetime.utcnow().date()
    first_day_of_current_month = today.replace(day=1)
    start = (first_day_of_current_month - timedelta(days=30 * months_back)).replace(day=1).isoformat()
    end = today.isoformat()

    response = client.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"]
    )

    total = 0.0
    for month_data in response["ResultsByTime"]:
        total += float(month_data["Total"]["UnblendedCost"]["Amount"])

    return {
        "start": start,
        "end": end,
        "currency": "USD",
        "totalCost": round(total, 2)
    }
