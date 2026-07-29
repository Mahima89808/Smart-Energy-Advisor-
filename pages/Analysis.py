"""
Analysis Page
Smart Energy Advisor

Responsibilities:
- Display appliance energy analysis
- Visualize analyzed data
- Call analysis utilities only
- Store analysis results for Suggestions page

No:
- Database logic
- API logic
- Energy calculations
- Knowledge base logic
"""

import pandas as pd
import streamlit as st

from utils.analyze_data import (
    analyze_appliances_dataframe,
    calculate_tariff
)

from utils.visualize import (
    create_consumption_pie_chart,
    create_consumption_bar_chart,
    create_cost_comparison_chart,
    create_bill_share_chart,
    create_daily_vs_monthly_chart
)


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Analysis - Energy Advisor",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Energy Consumption Analysis")

st.write(
    """
Analyze appliance electricity consumption,
monthly cost, bill contribution,
and estimated savings.
"""
)

st.divider()


# --------------------------------------------------
# Session Validation
# --------------------------------------------------

if (
    st.session_state.get("bill_data") is None
    or
    st.session_state.get("appliance_data") is None
):

    st.warning(
        "Upload both the electricity bill "
        "and appliance CSV on the Home page."
    )

    if st.button("← Back to Home"):

        st.switch_page(
            "pages/1_Home.py"
        )

    st.stop()


bill_data = st.session_state.bill_data

appliance_df = (
    st.session_state.appliance_data
    .copy()
)


# --------------------------------------------------
# Temporary Schema Adapter
# --------------------------------------------------

if "appliance" in appliance_df.columns:

    appliance_df = appliance_df.rename(
        columns={
            "appliance": "name"
        }
    )


if "category" not in appliance_df.columns:

    appliance_df["category"] = "Unknown"


# --------------------------------------------------
# Run Analysis
# --------------------------------------------------

analysis_df = analyze_appliances_dataframe(
    appliance_df,
    bill_data
)

st.session_state.analysis_data = analysis_df


# --------------------------------------------------
# Summary
# --------------------------------------------------

st.header("Analysis Summary")

total_units = (
    analysis_df["units_per_month"]
    .sum()
)

total_cost = (
    analysis_df["cost_per_month"]
    .sum()
)

average_units = (
    analysis_df["units_per_month"]
    .mean()
)

tariff = calculate_tariff(
    bill_data["total_amount"],
    bill_data["metered_units"]
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Monthly Units",
        f"{total_units:.2f} kWh"
    )

with col2:

    st.metric(
        "Estimated Cost",
        f"₹{total_cost:.2f}"
    )

with col3:

    st.metric(
        "Average / Appliance",
        f"{average_units:.2f} kWh"
    )

with col4:

    st.metric(
        "Tariff",
        f"₹{tariff:.2f}/kWh"
    )


st.divider()


# --------------------------------------------------
# Charts
# --------------------------------------------------

st.header("Energy Consumption")

left_chart, right_chart = st.columns(2)

with left_chart:

    pie_chart = create_consumption_pie_chart(
        analysis_df
    )

    st.plotly_chart(
        pie_chart,
        use_container_width=True
    )

with right_chart:

    bar_chart = create_consumption_bar_chart(
        analysis_df
    )

    st.plotly_chart(
        bar_chart,
        use_container_width=True
    )


st.divider()


# --------------------------------------------------
# Cost Analysis
# --------------------------------------------------

st.header("Cost Analysis")

cost_chart = create_cost_comparison_chart(
    analysis_df
)

st.plotly_chart(
    cost_chart,
    use_container_width=True
)


st.divider()


# --------------------------------------------------
# Bill Contribution
# --------------------------------------------------

st.header("Bill Contribution")

bill_share_chart = create_bill_share_chart(
    analysis_df
)

st.plotly_chart(
    bill_share_chart,
    use_container_width=True
)


st.divider()


# --------------------------------------------------
# Daily vs Monthly Consumption
# --------------------------------------------------

st.header("Daily vs Monthly Consumption")

daily_monthly_chart = create_daily_vs_monthly_chart(
    analysis_df
)

st.plotly_chart(
    daily_monthly_chart,
    use_container_width=True
)

st.divider()


# --------------------------------------------------
# Detailed Appliance Analysis
# --------------------------------------------------

st.header("Detailed Appliance Analysis")

display_df = analysis_df[
    [
        "name",
        "category",
        "wattage",
        "hours_per_day",
        "quantity",
        "units_per_day",
        "units_per_month",
        "cost_per_month",
        "bill_share",
        "monthly_saving",
        "yearly_saving"
    ]
].copy()

display_df = display_df.rename(
    columns={
        "name": "Appliance",
        "category": "Category",
        "wattage": "Wattage (W)",
        "hours_per_day": "Hours/Day",
        "quantity": "Quantity",
        "units_per_day": "Daily Units (kWh)",
        "units_per_month": "Monthly Units (kWh)",
        "cost_per_month": "Monthly Cost (₹)",
        "bill_share": "Bill Share (%)",
        "monthly_saving": "Monthly Saving (₹)",
        "yearly_saving": "Yearly Saving (₹)"
    }
)

display_df = display_df.sort_values(
    "Monthly Units (kWh)",
    ascending=False
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

st.divider()


# --------------------------------------------------
# Top Consumers
# --------------------------------------------------

st.header("Top Energy Consumers")

top_consumers = display_df.head(5)

for index, row in top_consumers.iterrows():

    with st.expander(
        f"⚡ {row['Appliance']}"
    ):

        left, right = st.columns(2)

        with left:

            st.metric(
                "Monthly Units",
                f"{row['Monthly Units (kWh)']:.2f} kWh"
            )

            st.metric(
                "Monthly Cost",
                f"₹{row['Monthly Cost (₹)']:.2f}"
            )

        with right:

            st.metric(
                "Bill Share",
                f"{row['Bill Share (%)']:.2f}%"
            )

            st.metric(
                "Estimated Yearly Saving",
                f"₹{row['Yearly Saving (₹)']:.2f}"
            )

st.divider()


# --------------------------------------------------
# Download Report
# --------------------------------------------------

st.header("Download Analysis")

csv = display_df.to_csv(
    index=False
)

st.download_button(
    label="📥 Download Analysis Report",
    data=csv,
    file_name="energy_analysis.csv",
    mime="text/csv"
)

st.divider()


# --------------------------------------------------
# Navigation
# --------------------------------------------------

left, right = st.columns(2)

with left:

    if st.button(
        "← Back to Home"
    ):

        st.switch_page(
            "pages/1_Home.py"
        )

with right:

    if st.button(
        "Suggestions →",
        type="primary"
    ):

        st.switch_page(
            "pages/3_Suggestions.py"
        )