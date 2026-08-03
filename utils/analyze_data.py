"""
Energy Analysis Engine

Responsible for:
- Electricity tariff calculation
- Appliance consumption calculation
- Appliance cost calculation
- Savings calculation
- DataFrame-based energy analysis

This module contains only mathematical calculations.

No:
- Database logic
- API logic
- UI logic
- Knowledge base logic
- Appliance-specific rules
"""

from typing import Dict, Any

import pandas as pd
import numpy as np


DAYS_IN_MONTH = 30


def calculate_tariff(
    total_amount: float,
    metered_units: float
) -> float:
    """
    Calculate electricity tariff from bill data.

    Formula:
        tariff = total_amount / metered_units

    Args:
        total_amount: Total electricity bill amount
        metered_units: Units consumed according to bill

    Returns:
        Cost per unit
    """

    if metered_units <= 0:
        return 0.0

    return round(total_amount / metered_units, 4)


def calculate_appliance_consumption(
    appliance_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate appliance energy consumption.

    Required columns:
        name
        category
        wattage
        hours_per_day
        quantity

    Adds:
        units_per_day
        units_per_month

    Formula:
        units_per_day =
        (wattage × hours_per_day × quantity) / 1000

        units_per_month =
        units_per_day × 30
    """

    required_columns = [
        "name",
        "category",
        "wattage",
        "hours_per_day",
        "quantity"
    ]

    for column in required_columns:
        if column not in appliance_df.columns:
            raise ValueError(
                f"Missing column: {column}"
            )

    df = appliance_df.copy()

    if (
        (df["wattage"] < 0).any()
        or
        (df["hours_per_day"] < 0).any()
        or
        (df["quantity"] < 0).any()
    ):
        raise ValueError(
            "Wattage, hours, and quantity cannot be negative"
        )

    df["units_per_day"] = (
        df["wattage"]
        *
        df["hours_per_day"]
        *
        df["quantity"]
    ) / 1000

    df["units_per_month"] = (
        df["units_per_day"]
        *
        DAYS_IN_MONTH
    )

    df["units_per_day"] = df["units_per_day"].round(4)

    df["units_per_month"] = (
        df["units_per_month"]
        .round(4)
    )

    return df

def scale_units_to_metered(
    appliance_df: pd.DataFrame,
    metered_units: float
) -> pd.DataFrame:
    """
    Scales each appliance's estimated units so the total across
    all appliances exactly matches the bill's real metered_units.

    Why: wattage x hours_per_day x quantity is only ever a rough
    estimate of real-world usage. Without this step, "Monthly
    Units" and "Estimated Cost" can drift far from the actual
    bill (e.g. if an appliance's assumed hours_per_day doesn't
    match how it was really used that period).

    This keeps each appliance's *relative* share of usage intact
    (an AC assumed to run 8x more than a fan still shows 8x more
    here) while forcing the *absolute* total to match reality.
    """

    df = appliance_df.copy()

    estimated_total = df["units_per_month"].sum()

    if estimated_total > 0 and metered_units > 0:
        scaling_factor = metered_units / estimated_total
    else:
        scaling_factor = 0.0

    df["units_per_day"] = (
        df["units_per_day"] * scaling_factor
    ).round(4)

    df["units_per_month"] = (
        df["units_per_month"] * scaling_factor
    ).round(4)

    return df

def calculate_appliance_cost(
    appliance_df: pd.DataFrame,
    per_unit_rate: float,
    total_bill: float
) -> pd.DataFrame:
    """
    Calculate appliance monthly cost
    and contribution to bill.

    Adds:
        cost_per_month
        bill_share
    """

    df = appliance_df.copy()

    df["cost_per_month"] = (
        df["units_per_month"]
        *
        per_unit_rate
    )

    if total_bill <= 0:
        df["bill_share"] = 0.0

    else:
        df["bill_share"] = (
            df["cost_per_month"]
            /
            total_bill
        ) * 100

    df["cost_per_month"] = (
        df["cost_per_month"]
        .round(2)
    )

    df["bill_share"] = (
        df["bill_share"]
        .round(2)
    )

    return df


def calculate_savings(
    monthly_cost: float,
    saving_percentage: float
) -> Dict[str, float]:
    """
    Calculate possible savings.

    Formula:

        monthly_saving =
        monthly_cost × saving_percentage / 100

        yearly_saving =
        monthly_saving × 12
    """

    if saving_percentage < 0:
        raise ValueError(
            "Saving percentage cannot be negative"
        )

    monthly_saving = (
        monthly_cost
        *
        saving_percentage
        /
        100
    )

    yearly_saving = (
        monthly_saving
        *
        12
    )

    return {
        "monthly_saving": round(
            monthly_saving,
            2
        ),
        "yearly_saving": round(
            yearly_saving,
            2
        )
    }


def analyze_appliances_dataframe(
    appliance_df: pd.DataFrame,
    bill_data: Dict[str, float],
    saving_percentage: float = 0
) -> pd.DataFrame:
    """
    Complete analysis for multiple appliances.

    Flow:

        Appliance DataFrame
                |
                ↓
        Consumption Calculation
                |
                ↓
        Bill Tariff Calculation
                |
                ↓
        Cost Calculation
                |
                ↓
        Savings Calculation
    """

    if "metered_units" not in bill_data:
        raise ValueError(
            "Missing metered_units"
        )

    if "total_amount" not in bill_data:
        raise ValueError(
            "Missing total_amount"
        )

    tariff = calculate_tariff(
        bill_data["total_amount"],
        bill_data["metered_units"]
    )

    df = calculate_appliance_consumption(
        appliance_df
    )

    df = scale_units_to_metered(
        df,
        bill_data["metered_units"]
    )

    df = calculate_appliance_cost(
        df,
        tariff,
        bill_data["total_amount"]
    )

    savings = (
        df["cost_per_month"]
        .apply(
            lambda cost:
            calculate_savings(
                cost,
                saving_percentage
            )
        )
    )

    df["monthly_saving"] = savings.apply(
        lambda x: x["monthly_saving"]
    )

    df["yearly_saving"] = savings.apply(
        lambda x: x["yearly_saving"]
    )

    df["per_unit_rate"] = tariff

    return df


def analyze_appliance(
    appliance: Dict[str, Any],
    bill_data: Dict[str, float],
    saving_percentage: float = 0
) -> Dict[str, Any]:
    """
    Analyze a single appliance.

    Used by suggestion engine.

    Returns:
        Dictionary containing analysis result.
    """

    appliance_df = pd.DataFrame(
        [appliance]
    )

    result_df = analyze_appliances_dataframe(
        appliance_df,
        bill_data,
        saving_percentage
    )

    result = (
        result_df
        .iloc[0]
        .to_dict()
    )

    return result