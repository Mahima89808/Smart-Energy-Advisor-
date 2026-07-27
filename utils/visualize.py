"""
Smart Energy Advisor
Visualization Utilities

Responsibilities:
- Generate Plotly visualizations
- Display analyzed appliance data

No:
- Database logic
- API logic
- Energy calculations
- Knowledge base logic
- Appliance matching

Input:
An already analyzed DataFrame produced by utils.analyze_data.
"""

from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def _require_columns(df: pd.DataFrame, columns: list[str]) -> None:
    """
    Validate that the required columns exist.
    """
    missing = [column for column in columns if column not in df.columns]

    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(missing)}"
        )


def create_consumption_pie_chart(
    appliance_df: pd.DataFrame
) -> go.Figure:
    """
    Pie chart of monthly energy consumption.
    """

    _require_columns(
        appliance_df,
        ["name", "units_per_month"]
    )

    fig = px.pie(
        appliance_df,
        names="name",
        values="units_per_month",
        title="Monthly Energy Consumption Distribution",
        hole=0.35
    )

    fig.update_traces(
        textinfo="percent+label",
        hovertemplate=(
            "<b>%{label}</b>"
            "<br>Consumption: %{value:.2f} kWh"
            "<br>%{percent}<extra></extra>"
        )
    )

    return fig


def create_consumption_bar_chart(
    appliance_df: pd.DataFrame
) -> go.Figure:
    """
    Monthly energy consumption by appliance.
    """

    _require_columns(
        appliance_df,
        ["name", "units_per_month"]
    )

    df = appliance_df.sort_values(
        "units_per_month",
        ascending=False
    )

    fig = px.bar(
        df,
        x="name",
        y="units_per_month",
        title="Monthly Energy Consumption",
        labels={
            "name": "Appliance",
            "units_per_month": "Monthly Units (kWh)"
        }
    )

    fig.update_layout(
        xaxis_tickangle=-45
    )

    return fig


def create_cost_comparison_chart(
    appliance_df: pd.DataFrame
) -> go.Figure:
    """
    Monthly appliance cost comparison.
    """

    _require_columns(
        appliance_df,
        ["name", "cost_per_month"]
    )

    df = appliance_df.sort_values(
        "cost_per_month",
        ascending=False
    )

    fig = px.bar(
        df,
        x="name",
        y="cost_per_month",
        title="Monthly Electricity Cost by Appliance",
        labels={
            "name": "Appliance",
            "cost_per_month": "Monthly Cost"
        }
    )

    fig.update_layout(
        xaxis_tickangle=-45
    )

    return fig


def create_bill_share_chart(
    appliance_df: pd.DataFrame
) -> go.Figure:
    """
    Percentage contribution of each appliance
    to the total electricity bill.
    """

    _require_columns(
        appliance_df,
        ["name", "bill_share"]
    )

    fig = px.bar(
        appliance_df.sort_values(
            "bill_share",
            ascending=False
        ),
        x="name",
        y="bill_share",
        title="Bill Contribution by Appliance",
        labels={
            "name": "Appliance",
            "bill_share": "Bill Share (%)"
        }
    )

    fig.update_layout(
        xaxis_tickangle=-45
    )

    return fig


def create_daily_vs_monthly_chart(
    appliance_df: pd.DataFrame
) -> go.Figure:
    """
    Compare daily and monthly consumption.
    """

    _require_columns(
        appliance_df,
        [
            "name",
            "units_per_day",
            "units_per_month"
        ]
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="Daily",
            x=appliance_df["name"],
            y=appliance_df["units_per_day"]
        )
    )

    fig.add_trace(
        go.Bar(
            name="Monthly",
            x=appliance_df["name"],
            y=appliance_df["units_per_month"]
        )
    )

    fig.update_layout(
        title="Daily vs Monthly Energy Consumption",
        barmode="group",
        xaxis_title="Appliance",
        yaxis_title="Energy (kWh)",
        xaxis_tickangle=-45
    )

    return fig


def create_savings_projection_chart(
    current_cost: float,
    projected_cost: float
) -> go.Figure:
    """
    Compare current cost with projected cost.
    """

    savings = current_cost - projected_cost

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=[
                "Current",
                "Projected",
                "Savings"
            ],
            y=[
                current_cost,
                projected_cost,
                savings
            ]
        )
    )

    fig.update_layout(
        title="Monthly Cost Savings Projection",
        yaxis_title="Amount"
    )

    return fig


def create_gauge_chart(
    value: float,
    maximum: float,
    title: Optional[str] = "Efficiency Score"
) -> go.Figure:
    """
    Generic gauge visualization.
    """

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title},
            gauge={
                "axis": {
                    "range": [0, maximum]
                }
            }
        )
    )

    return fig