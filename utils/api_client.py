"""
API Client
Smart Energy Advisor

Responsibilities:
- Communicate with the FastAPI backend
- Send HTTP requests
- Return JSON responses

No:
- Streamlit code
- Business logic
- Database logic
- Data analysis
- Data formatting
"""

from typing import Any, Dict, List, Optional

import requests


# --------------------------------------------------
# Configuration
# --------------------------------------------------

API_BASE_URL = "http://127.0.0.1:8000"

DEFAULT_TIMEOUT = 30


# --------------------------------------------------
# Internal Request Helper
# --------------------------------------------------

def _request(
    method: str,
    endpoint: str,
    **kwargs
):
    """
    Sends an HTTP request to the FastAPI backend.

    Raises:
        requests.HTTPError
        requests.ConnectionError
        requests.Timeout
    """

    url = f"{API_BASE_URL}{endpoint}"

    response = requests.request(
        method=method,
        url=url,
        timeout=DEFAULT_TIMEOUT,
        **kwargs
    )

    try:
        response.raise_for_status()
    except requests.HTTPError:
        try:
            detail = response.json().get("detail")
        except Exception:
            detail = response.text

        raise RuntimeError(detail)

    return response.json()


# --------------------------------------------------
# Bill Extraction
# --------------------------------------------------

def extract_bill_pdf(file):
    return _request(
        "POST",
        "/extract-bill",
        files={
            "file": (
                file.name,
                file,
                "application/pdf"
            )
        }
    )



def extract_bill_csv(file):
    return _request(
        "POST",
        "/extract-bill/csv",
        files={
            "file": (
                file.name,
                file,
                "text/csv"
            )
        }
    )


def extract_bill_manual(
    bill_data: Dict[str, Any]
):
    return _request(
        "POST",
        "/extract-bill/manual",
        json=bill_data
    )


# --------------------------------------------------
# Appliance CRUD
# --------------------------------------------------

def get_appliances():
    return _request(
        "GET",
        "/appliances"
    )


def create_appliance(
    appliance: Dict[str, Any]
):
    return _request(
        "POST",
        "/appliances",
        json=appliance
    )


def update_appliance(
    appliance_id: int,
    appliance: Dict[str, Any]
):
    return _request(
        "PUT",
        f"/appliances/{appliance_id}",
        json=appliance
    )


def delete_appliance(
    appliance_id: int
):
    return _request(
        "DELETE",
        f"/appliances/{appliance_id}"
    )


# --------------------------------------------------
# Suggestions
# --------------------------------------------------

def generate_energy_suggestions(
    appliances: List[Dict[str, Any]],
    bill_data: Dict[str, Any]
):
    return _request(
        "POST",
        "/suggestions",
        json={
            "appliances": appliances,
            "bill_data": bill_data
        }
    )


# --------------------------------------------------
# Saved Records
# --------------------------------------------------

def save_record(
    bill_data: Dict[str, Any],
    appliance_snapshot: List[Dict[str, Any]]
):
    return _request(
        "POST",
        "/saved-records",
        json={
            "bill_data": bill_data,
            "appliance_snapshot": appliance_snapshot
        }
    )


def get_saved_records():
    return _request(
        "GET",
        "/saved-records"
    )


def get_saved_record(
    record_id: int
):
    return _request(
        "GET",
        f"/saved-records/{record_id}"
    )


def rename_saved_record(
    record_id: int,
    label: str
):
    return _request(
        "PATCH",
        f"/saved-records/{record_id}",
        json={
            "label": label
        }
    )


def delete_saved_record(
    record_id: int
):
    return _request(
        "DELETE",
        f"/saved-records/{record_id}"
    )