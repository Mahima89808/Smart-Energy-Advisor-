from utils.suggestions import generate_suggestion
from utils.appliance_matcher import match_appliance


bill = {
    "metered_units": 300,
    "total_amount": 1800
}


appliance = {
    "name": "fridge",
    "category": "Kitchen",
    "wattage": 200,
    "hours_per_day": 24,
    "quantity": 1
}


print(match_appliance("fridge"))


result = generate_suggestion(
    appliance,
    bill
)


print(result)