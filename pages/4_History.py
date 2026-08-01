"""
History Page
Smart Energy Advisor

Responsibilities:
- List previously saved analysis records
- Recompute analysis from a saved snapshot (bill + appliances)
- Reuse the same visualization functions as the Analysis page
- Rename and delete saved records

No:
- New energy calculations (recomputation reuses utils/analyze_data.py)
- Database logic (all reads/writes go through utils/api_client.py)
- Duplicated business logic
"""

import pandas as pd
import requests
import streamlit as st

from utils.api_client import (
    get_saved_records,
    get_saved_record,
    rename_saved_record,
    delete_saved_record
)

from utils.analyze_data import analyze_appliances_dataframe, calculate_tariff

from utils.visualize import (
    create_consumption_pie_chart,
    create_consumption_bar_chart,
    create_cost_comparison_chart,
    create_bill_share_chart,
    create_daily_vs_monthly_chart
)

from utils.sidebar import render_sidebar


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="History - Energy Advisor",
    page_icon="📚",
    layout="wide"
)

render_sidebar()
session_id = st.session_state.session_id

st.title("📚 Analysis History")

st.write(
    """
Browse previously saved analyses. Selecting a record
recomputes its full analysis from the saved bill and
appliance snapshot, using the same engine as the Analysis page.
"""
)

st.divider()


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "history_selected_id" not in st.session_state:
    st.session_state.history_selected_id = None


# --------------------------------------------------
# Load Saved Records
# --------------------------------------------------

try:

    records = get_saved_records(session_id)

except requests.ConnectionError:

    st.error(
        "Cannot connect to the backend.\n\n"
        "Start FastAPI using:\n\n"
        "uvicorn backend.main:app --reload"
    )
    st.stop()

except Exception as error:

    st.error(str(error))
    st.stop()


# ==================================================
# LIST VIEW
# ==================================================

if st.session_state.history_selected_id is None:

    if not records:

        st.info("No saved analyses yet. Save one from the Suggestions page.")

    else:

        st.header(f"Saved Analyses ({len(records)})")

        for record in records:

            with st.container(border=True):

                left, middle, right = st.columns([3, 2, 1])

                with left:

                    st.markdown(f"**{record['label']}**")

                    st.caption(
                        f"{record.get('consumer_name') or 'N/A'} • "
                        f"{record.get('bill_month') or 'N/A'}"
                    )

                with middle:

                    st.metric(
                        "Total Amount",
                        f"₹{(record.get('total_amount') or 0):.2f}"
                    )

                    st.caption(f"Saved: {record['saved_at'][:10]}")

                with right:

                    if st.button(
                        "View →",
                        key=f"view_{record['id']}"
                    ):

                        st.session_state.history_selected_id = record["id"]
                        st.rerun()


# ==================================================
# DETAIL VIEW
# ==================================================

else:

    record_id = st.session_state.history_selected_id

    try:
        detail = get_saved_record(session_id, record_id)

    except RuntimeError as error:

        st.error(str(error))
        st.session_state.history_selected_id = None
        st.stop()

    except requests.ConnectionError:

        st.error(
            "Cannot connect to the backend.\n\n"
            "Start FastAPI using:\n\n"
            "uvicorn backend.main:app --reload"
        )
        st.stop()

    except Exception as error:

        st.error(str(error))
        st.stop()

    record = detail["record"]
    appliances = detail["appliances"]

    if st.button("← Back to List"):

        st.session_state.history_selected_id = None
        st.rerun()

    st.header(f"📄 {record['label']}")


    # ----------------------------------------
    # Rename / Delete controls
    # ----------------------------------------

    rename_col, delete_col = st.columns(2)

    with rename_col:

        new_label = st.text_input(
            "Rename this record",
            value=record["label"],
            key=f"rename_input_{record_id}"
        )

        if st.button("Save Label", key=f"rename_btn_{record_id}"):

            try:
                rename_saved_record(session_id, record_id, new_label)
                st.success("Label updated.")
                st.rerun()

            except Exception as error:
                st.error(str(error))

    with delete_col:

        st.write("")
        st.write("")

        if st.button(
            "🗑 Delete This Record",
            key=f"delete_btn_{record_id}"
        ):

            try:
                delete_saved_record(session_id, record_id)
                st.session_state.history_selected_id = None
                st.success("Record deleted.")
                st.rerun()

            except Exception as error:
                st.error(str(error))

    st.divider()


    # ----------------------------------------
    # Bill Snapshot
    # ----------------------------------------

    st.subheader("Bill Snapshot")

    info_left, info_right = st.columns(2)

    with info_left:

        st.metric("Consumer Number", record.get("consumer_no") or "N/A")
        st.metric("Consumer Name", record.get("consumer_name") or "N/A")
        st.metric("Bill Month", record.get("bill_month") or "N/A")
        st.metric("Billing Date", record.get("billing_date") or "N/A")

    with info_right:

        st.metric("Due Date", record.get("due_date") or "N/A")
        st.metric("Metered Units", f"{(record.get('metered_units') or 0):.2f} kWh")
        st.metric("Total Amount", f"₹{(record.get('total_amount') or 0):.2f}")
        st.metric("Previous Reading", record.get("previous_reading") or "N/A")

    st.divider()


    # ----------------------------------------
    # Recompute Analysis From Snapshot
    # ----------------------------------------

    if not appliances:

        st.warning("This record has no appliance snapshot to analyze.")

    else:

        appliance_df = pd.DataFrame(appliances)[
            ["name", "category", "wattage", "hours_per_day", "quantity"]
        ]

        bill_data = {
            "metered_units": record.get("metered_units") or 0,
            "total_amount": record.get("total_amount") or 0
        }

        analysis_df = analyze_appliances_dataframe(appliance_df, bill_data)

        st.subheader("Analysis Summary")

        total_units = analysis_df["units_per_month"].sum()
        total_cost = analysis_df["cost_per_month"].sum()
        average_units = analysis_df["units_per_month"].mean()

        tariff = calculate_tariff(
            bill_data["total_amount"],
            bill_data["metered_units"]
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Monthly Units", f"{total_units:.2f} kWh")

        with col2:
            st.metric("Estimated Cost", f"₹{total_cost:.2f}")

        with col3:
            st.metric("Average / Appliance", f"{average_units:.2f} kWh")

        with col4:
            st.metric("Tariff", f"₹{tariff:.2f}/kWh")

        st.divider()


        # ----------------------------------------
        # Charts
        # ----------------------------------------

        st.subheader("Energy Consumption")

        left_chart, right_chart = st.columns(2)

        with left_chart:

            st.plotly_chart(
                create_consumption_pie_chart(analysis_df),
                use_container_width=True
            )

        with right_chart:

            st.plotly_chart(
                create_consumption_bar_chart(analysis_df),
                use_container_width=True
            )

        st.subheader("Cost Analysis")

        st.plotly_chart(
            create_cost_comparison_chart(analysis_df),
            use_container_width=True
        )

        st.subheader("Bill Contribution")

        st.plotly_chart(
            create_bill_share_chart(analysis_df),
            use_container_width=True
        )

        st.subheader("Daily vs Monthly Consumption")

        st.plotly_chart(
            create_daily_vs_monthly_chart(analysis_df),
            use_container_width=True
        )

        st.divider()


        # ----------------------------------------
        # Detailed Table
        # ----------------------------------------

        st.subheader("Detailed Appliance Analysis")

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
                "bill_share"
            ]
        ].rename(
            columns={
                "name": "Appliance",
                "category": "Category",
                "wattage": "Wattage (W)",
                "hours_per_day": "Hours/Day",
                "quantity": "Quantity",
                "units_per_day": "Daily Units (kWh)",
                "units_per_month": "Monthly Units (kWh)",
                "cost_per_month": "Monthly Cost (₹)",
                "bill_share": "Bill Share (%)"
            }
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


# --------------------------------------------------
# Navigation
# --------------------------------------------------

st.divider()

left_nav, right_nav = st.columns(2)

with left_nav:

    if st.button("← Back to Suggestions", key="bottom_back_suggestions"):

        st.switch_page("pages/3_Suggestions.py")

with right_nav:

    if st.button("Home →", type="primary", key="bottom_about"):

        st.switch_page("pages/1_Home.py")