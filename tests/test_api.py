"""
API Tests

Tests the FastAPI backend endpoints.

Responsibilities:
- Verify endpoint responses
- Verify request validation
- Verify HTTP status codes

No UI testing.
No database implementation testing.
No business logic duplication.
"""

import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.main import app


client = TestClient(app)

FIXTURES = Path(__file__).resolve().parent / "fixtures"


# --------------------------------------------------
# Bill Extraction
# --------------------------------------------------

def test_extract_bill_invalid_pdf_returns_400():
    response = client.post(
        "/extract-bill",
        files={
            "file": (
                "bill.pdf",
                b"not a valid pdf",
                "application/pdf"
            )
        }
    )

    assert response.status_code == 400


def test_extract_bill_pdf_returns_200():
    with open(FIXTURES / "sample_bill.pdf", "rb") as file:

        response = client.post(
            "/extract-bill",
            files={
                "file": (
                    "sample_bill.pdf",
                    file,
                    "application/pdf"
                )
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["consumer_no"] == "123456789"
    assert data["metered_units"] == 300.0


def test_extract_bill_image_returns_200():
    with open(FIXTURES / "sample_bill.png", "rb") as file:

        response = client.post(
            "/extract-bill/image",
            files={
                "file": (
                    "sample_bill.png",
                    file,
                    "image/png"
                )
            }
        )

    assert response.status_code == 200

    assert response.json()["consumer_no"] == "987654321"


def test_extract_bill_csv_returns_200():
    csv_content = (
        "metered_units,total_amount\n"
        "300,2500\n"
    )

    response = client.post(
        "/extract-bill/csv",
        files={
            "file": (
                "bill.csv",
                csv_content.encode(),
                "text/csv"
            )
        }
    )

    assert response.status_code == 200

    assert response.json()["metered_units"] == 300.0


def test_extract_bill_manual_returns_200():
    response = client.post(
        "/extract-bill/manual",
        json={
            "metered_units": 300,
            "total_amount": 2500
        }
    )

    assert response.status_code == 200

    assert response.json()["metered_units"] == 300.0


# --------------------------------------------------
# Appliance CRUD
# --------------------------------------------------

def test_appliance_crud():
    create_response = client.post(
        "/appliances",
        json={
            "name": "Fan",
            "category": "Cooling",
            "wattage": 75,
            "hours_per_day": 8,
            "quantity": 2
        }
    )

    assert create_response.status_code == 200

    appliance_id = create_response.json()["id"]

    list_response = client.get("/appliances")

    assert list_response.status_code == 200

    update_response = client.put(
        f"/appliances/{appliance_id}",
        json={
            "name": "Ceiling Fan",
            "category": "Cooling",
            "wattage": 75,
            "hours_per_day": 10,
            "quantity": 2
        }
    )

    assert update_response.status_code == 200

    delete_response = client.delete(
        f"/appliances/{appliance_id}"
    )

    assert delete_response.status_code == 200


# --------------------------------------------------
# Suggestions
# --------------------------------------------------

def test_generate_suggestions():
    response = client.post(
        "/suggestions",
        json={
            "bill_data": {
                "metered_units": 300,
                "total_amount": 2500
            },
            "appliances": [
                {
                    "name": "Fan",
                    "category": "Cooling",
                    "wattage": 75,
                    "hours_per_day": 8,
                    "quantity": 2
                }
            ]
        }
    )

    assert response.status_code == 200

    result = response.json()

    assert isinstance(result, list)

    assert len(result) == 1

    assert "suggestion" in result[0]


# --------------------------------------------------
# Saved Records
# --------------------------------------------------

def test_saved_record_crud():
    create_response = client.post(
        "/saved-records",
        json={
            "bill_data": {
                "metered_units": 300,
                "total_amount": 2500
            },
            "appliance_snapshot": []
        }
    )

    assert create_response.status_code == 200

    record_id = create_response.json()["id"]

    list_response = client.get(
        "/saved-records"
    )

    assert list_response.status_code == 200

    detail_response = client.get(
        f"/saved-records/{record_id}"
    )

    assert detail_response.status_code == 200

    rename_response = client.patch(
        f"/saved-records/{record_id}",
        json={
            "label": "Unit Test Record"
        }
    )

    assert rename_response.status_code == 200

    delete_response = client.delete(
        f"/saved-records/{record_id}"
    )

    assert delete_response.status_code == 200