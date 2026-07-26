from utils.analyze_data import analyze_appliances_dataframe


appliances = [
    {
        "name": "Fan",
        "category": "Cooling",
        "wattage": 75,
        "hours_per_day": 8,
        "quantity": 2
    },
    {
        "name": "TV",
        "category": "Entertainment",
        "wattage": 100,
        "hours_per_day": 5,
        "quantity": 1
    }
]


bill = {
    "metered_units": 300,
    "total_amount": 1800
}


import pandas as pd

df = pd.DataFrame(appliances)

result = analyze_appliances_dataframe(
    df,
    bill,
    saving_percentage=20
)

print(result)