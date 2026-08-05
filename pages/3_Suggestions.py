"""
Suggestions Page
Smart Energy Advisor

Responsibilities:
- Request energy-saving suggestions from the backend
- Display personalized recommendations
- Display estimated savings returned by the backend

No:
- Energy calculations
- Appliance matching
- Business logic
- Database logic
"""

import streamlit as st
import pandas as pd
import requests

from utils.api_client import generate_energy_suggestions, save_record
from utils.sidebar import render_sidebar

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Suggestions - Energy Advisor",
    page_icon="💡",
    layout="wide"
)

render_sidebar()
session_id = st.session_state.session_id

st.title("💡 Energy Saving Suggestions")

st.write(
    """
Personalized recommendations generated
by the Smart Energy Advisor backend.
"""
)

st.divider()


# --------------------------------------------------
# Session Validation
# --------------------------------------------------

if (
    st.session_state.get("analysis_data") is None
    or
    st.session_state.get("bill_data") is None
):

    st.warning(
        "Complete the analysis before viewing suggestions."
    )

    if st.button("← Back to Analysis"):

        st.switch_page(
            "pages/2_Analysis.py"
        )

    st.stop()


analysis_df = (
    st.session_state.analysis_data
    .copy()
)

bill_data = (
    st.session_state.bill_data
)


# --------------------------------------------------
# Request Suggestions
# --------------------------------------------------

try:

    suggestions = generate_energy_suggestions(

        analysis_df.to_dict(
            orient="records"
        ),

        bill_data

    )

except requests.ConnectionError:

    st.error(
        "Cannot connect to the backend.\n\n"
        "Start FastAPI using:\n\n"
        "uvicorn backend.main:app --reload"
    )

    st.stop()

except RuntimeError as error:

    st.error(str(error))

    st.stop()

except Exception as error:

    st.error(str(error))

    st.stop()


# --------------------------------------------------
# Overview
# --------------------------------------------------

st.header("Recommendation Summary")

total_monthly_saving = sum(
    item["monthly_saving"]
    for item in suggestions
)

total_yearly_saving = sum(
    item["yearly_saving"]
    for item in suggestions
)

average_saving = 0

if suggestions:

    average_saving = (
        sum(
            item["saving_percentage"]
            for item in suggestions
        )
        /
        len(suggestions)
    )

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Recommendations",
        len(suggestions)
    )

with col2:

    st.metric(
        "Estimated Monthly Saving",
        f"₹{total_monthly_saving:.2f}"
    )

with col3:

    st.metric(
        "Estimated Yearly Saving",
        f"₹{total_yearly_saving:.2f}"
    )


st.metric(
    "Average Saving Percentage",
    f"{average_saving:.1f}%"
)

st.divider()



# --------------------------------------------------
# Personalized Recommendations
# --------------------------------------------------

st.header("Personalized Recommendations")

if not suggestions:

    st.success(
        "No recommendations were generated."
    )

else:

    for index, suggestion in enumerate(
        suggestions,
        start=1
    ):

        with st.expander(
            f"{index}. {suggestion['appliance']}"
        ):

            left_column, right_column = st.columns(2)

            with left_column:

                st.metric(
                    "Category",
                    suggestion["category"]
                )

                st.metric(
                    "Monthly Consumption",
                    f"{suggestion['units_per_month']:.2f} kWh"
                )

                st.metric(
                    "Monthly Cost",
                    f"₹{suggestion['cost_per_month']:.2f}"
                )

                st.metric(
                    "Bill Share",
                    f"{suggestion['bill_share']:.2f}%"
                )

            with right_column:

                st.metric(
                    "Matched Rule",
                    suggestion["matched_rule"]
                )

                st.metric(
                    "Match Type",
                    suggestion["match_type"].title()
                )

                st.metric(
                    "Estimated Saving",
                    f"{suggestion['saving_percentage']}%"
                )

                st.metric(
                    "Monthly Saving",
                    f"₹{suggestion['monthly_saving']:.2f}"
                )

                st.metric(
                    "Yearly Saving",
                    f"₹{suggestion['yearly_saving']:.2f}"
                )

            st.markdown("### Recommendation")

            st.success(
                suggestion["suggestion"]
            )

            st.divider()


# --------------------------------------------------
# Savings Summary
# --------------------------------------------------

st.header("Potential Savings")

summary_df = pd.DataFrame(suggestions)

summary_df = summary_df[
    [
        "appliance",
        "saving_percentage",
        "monthly_saving",
        "yearly_saving"
    ]
].rename(
    columns={
        "appliance": "Appliance",
        "saving_percentage": "Saving (%)",
        "monthly_saving": "Monthly Saving (₹)",
        "yearly_saving": "Yearly Saving (₹)"
    }
)

st.dataframe(
    summary_df,
    width="stretch",
    hide_index=True
)

st.download_button(
    label="📥 Download Suggestions Report",
    data=summary_df.to_csv(index=False),
    file_name="energy_suggestions.csv",
    mime="text/csv"
)

st.divider()


# --------------------------------------------------
# Save Analysis
# --------------------------------------------------

st.header("Save This Analysis")

st.write(
    "Save this bill and appliance analysis so you can "
    "revisit it later from the History page."
)

if st.button(
    "💾 Save This Analysis",
    type="primary"
):

    try:

        appliance_snapshot = analysis_df.to_dict(
            orient="records"
        )

        result = save_record(
            session_id,
            bill_data,
            appliance_snapshot
        )

        st.success(
            f"Analysis saved (record ID: {result['id']})."
        )

    except requests.ConnectionError:

        st.error(
            "Cannot connect to the backend.\n\n"
            "Start FastAPI using:\n\n"
            "uvicorn backend.main:app --reload"
        )

    except RuntimeError as error:

        st.error(str(error))

    except Exception as error:

        st.error(str(error))

st.divider()


# --------------------------------------------------
# Navigation
# --------------------------------------------------

left_column, right_column = st.columns(2)

with left_column:

    if st.button(
        "← Back to Analysis"
    ):

        st.switch_page(
            "pages/2_Analysis.py"
        )

with right_column:

    if st.button(
        "History →",
        type="primary"
    ):

        st.switch_page(
            "pages/4_History.py"
        )