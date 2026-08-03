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

import pandas as pd

from utils.analyze_data import analyze_appliances_dataframe, calculate_savings
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
    Generate suggestion for one appliance, analyzed in isolation.

    NOTE: kept for backward compatibility (e.g. tests that call it
    directly). Not used internally by generate_suggestions anymore,
    since analyzing a single appliance in isolation causes its units
    to be incorrectly scaled up to the full bill's metered units. Use
    generate_suggestions() for correct, bill-reconciled results across
    a full appliance list.
    """

    from utils.analyze_data import analyze_appliance

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

    Analyzes the whole appliance list together first, so units and
    cost are correctly scaled against the real bill total (not each
    appliance individually pretending it's the only one on the bill).
    Then matches each appliance to a rule and applies that specific
    appliance's own saving_percentage on top of the shared, correctly
    reconciled analysis.
    """

    if not appliances:
        return []

    appliance_df = pd.DataFrame(appliances)

    analyzed_df = analyze_appliances_dataframe(
        appliance_df,
        bill_data
    )

    results = []

    for _, row in analyzed_df.iterrows():

        appliance = row.to_dict()

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

        savings = calculate_savings(
            appliance["cost_per_month"],
            saving_percentage
        )

        analysis = dict(appliance)
        analysis["monthly_saving"] = savings["monthly_saving"]
        analysis["yearly_saving"] = savings["yearly_saving"]

        results.append(
            format_suggestion(
                appliance,
                match_result,
                analysis
            )
        )

    return results