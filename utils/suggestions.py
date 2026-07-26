"""
Suggestion Engine

Responsible for:
- Connecting appliance matcher with analysis engine
- Generating energy-saving suggestions
- Calculating estimated savings

No:
- Appliance-specific rules
- Hardcoded suggestions
- Database logic
- UI logic

Knowledge comes from:
knowledge/appliance_rules.json
through appliance_matcher.py
"""

from typing import Dict, List, Any

from utils.analyze_data import analyze_appliance
from utils.appliance_matcher import match_appliance


def format_suggestion(
    appliance: Dict[str, Any],
    match_result: Dict[str, Any],
    analysis: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Format final suggestion response.
    """

    rule = match_result.get(
        "rule",
        {}
    )

    suggestion = rule.get(
        "suggestion",
        {}
    )

    return {
        "appliance": appliance.get(
            "name",
            ""
        ),

        "category": appliance.get(
            "category",
            ""
        ),

        "matched_rule": match_result.get(
            "matched_name",
            "generic"
        ),

        "match_type": match_result.get(
            "match_type",
            "fallback"
        ),

        "suggestion": suggestion.get(
            "action",
            "Reduce unnecessary usage and improve efficiency."
        ),

        "saving_percentage": suggestion.get(
            "saving_percentage",
            0
        ),

        "units_per_month": analysis.get(
            "units_per_month",
            0
        ),

        "cost_per_month": analysis.get(
            "cost_per_month",
            0
        ),

        "bill_share": analysis.get(
            "bill_share",
            0
        ),

        "monthly_saving": analysis.get(
            "monthly_saving",
            0
        ),

        "yearly_saving": analysis.get(
            "yearly_saving",
            0
        )
    }


def generate_suggestion(
    appliance: Dict[str, Any],
    bill_data: Dict[str, float]
) -> Dict[str, Any]:
    """
    Generate suggestion for one appliance.
    """

    match_result = match_appliance(
        appliance.get(
            "name",
            ""
        )
    )

    if not match_result:
        match_result = {
            "match_type": "fallback",
            "matched_name": "generic",
            "rule": {
                "suggestion": {
                    "action":
                        "Reduce unnecessary usage and improve efficiency.",
                    "saving_percentage": 0
                }
            }
        }

    rule = match_result.get(
        "rule",
        {}
    )

    suggestion = rule.get(
        "suggestion",
        {}
    )

    saving_percentage = suggestion.get(
        "saving_percentage",
        0
    )

    analysis = analyze_appliance(
        appliance,
        bill_data,
        saving_percentage
    )

    return format_suggestion(
        appliance,
        match_result,
        analysis
    )


def generate_suggestions(
    appliances: List[Dict[str, Any]],
    bill_data: Dict[str, float]
) -> List[Dict[str, Any]]:
    """
    Generate suggestions for multiple appliances.
    """

    results = []

    for appliance in appliances:
        results.append(
            generate_suggestion(
                appliance,
                bill_data
            )
        )

    return results