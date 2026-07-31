import requests

payload = {
    "bill_data": {
        "consumer_no": "123456789",
        "consumer_name": "John Doe",
        "bill_month": "July 2026",
        "billing_date": "01/07/2026",
        "due_date": "15/07/2026",
        "metered_units": 300,
        "total_amount": 2500,
        "previous_reading": 1000,
        "current_reading": 1300
    },
    "appliances": [
        {"name": "Fan", "category": "Cooling", "wattage": 75, "hours_per_day": 8, "quantity": 2}
    ]
}

response = requests.post("http://127.0.0.1:8000/suggestions", json=payload)

print("STATUS:", response.status_code)
print("BODY:", response.text)