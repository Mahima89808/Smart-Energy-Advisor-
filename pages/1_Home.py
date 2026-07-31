"""
Home Page
Smart Energy Advisor
 
Responsibilities:
- Upload electricity bills
- Upload appliance CSV
- Call FastAPI through api_client
- Store extracted data in Streamlit session
 
No:
- PDF extraction logic
- OCR logic
- Database logic
- Business logic
"""
 
import os
 
import pandas as pd
import requests
import streamlit as st
 
from utils.api_client import (
    extract_bill_pdf,
    extract_bill_csv,
    extract_bill_manual,
)
from utils.sidebar import render_sidebar
 
 
# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
 
st.set_page_config(
    page_title="Home - Energy Advisor",
    page_icon="🏠",
    layout="wide"
)

render_sidebar()
 
st.title("🏠 Home - Upload & Extract Data")
 
st.write(
    """
Upload your electricity bill and appliance information
to begin your electricity consumption analysis.
"""
)
 
st.divider()
 
 
# --------------------------------------------------
# Session State
# --------------------------------------------------
 
if "bill_data" not in st.session_state:
    st.session_state.bill_data = None
 
if "appliance_data" not in st.session_state:
    st.session_state.appliance_data = None
 
 
# --------------------------------------------------
# Layout
# --------------------------------------------------
 
left_column, right_column = st.columns(2)
 
 
# ==================================================
# LEFT COLUMN
# Electricity Bill
# ==================================================
 
with left_column:

    with st.container(border=True):

        st.subheader("📄 Electricity Bill")
        bill_input_method = st.radio(
            "Bill Input Method",
            [
                "PDF",
                "CSV",
                "Manual"
            ],
            horizontal=True
        )

        if bill_input_method == "PDF":
            uploaded_bill = st.file_uploader(
                "Upload PDF Bill",
                type=["pdf"],
                key="pdf_bill",
            )


        elif bill_input_method == "CSV":
            uploaded_bill = st.file_uploader(
                "Upload Bill CSV",
                type=["csv"],
                key="csv_bill",
            )

        else:
            uploaded_bill = None

        if uploaded_bill is not None:

            try:

                with st.spinner("Extracting bill data..."):

                    if bill_input_method == "PDF":
                        bill_data = extract_bill_pdf(uploaded_bill)

                    elif bill_input_method == "Image":
                        bill_data = extract_bill_image(uploaded_bill)

                    elif bill_input_method == "CSV":
                        bill_data = extract_bill_csv(uploaded_bill)

                    st.session_state.bill_data = bill_data

                st.success("Bill extracted successfully.")

            except requests.ConnectionError:

                st.error(
                    "Cannot connect to the backend.\n\n"
                    "Start FastAPI using:\n\n"
                    "uvicorn backend.main:app --reload"
                )

            except requests.HTTPError as error:

                try:
                    detail = error.response.json()["detail"]
                except Exception:
                    detail = str(error)

                st.error(detail)

            except Exception as error:

                st.error(str(error))

        if st.session_state.bill_data:

            bill = st.session_state.bill_data

            st.markdown("### Extracted Bill Information")

            info_left, info_right = st.columns(2)

            with info_left:

                st.metric(
                    "Consumer Number",
                    bill["consumer_no"]
                )

                st.metric(
                    "Consumer Name",
                    bill["consumer_name"]
                )

                st.metric(
                    "Bill Month",
                    bill["bill_month"]
                )

                st.metric(
                    "Billing Date",
                    bill["billing_date"]
                )

            with info_right:

                st.metric(
                    "Due Date",
                    bill["due_date"]
                )

                st.metric(
                    "Metered Units",
                    f"{bill['metered_units']:.2f} kWh"
                )

                st.metric(
                    "Total Amount",
                    f"₹{bill['total_amount']:.2f}"
                )

                st.metric(
                    "Previous Reading",
                    bill["previous_reading"]
                )

                st.metric(
                    "Current Reading",
                    bill["current_reading"]
                )
 
 
# ==================================================
# RIGHT COLUMN
# Appliance CSV
# ==================================================
 
with right_column:

    with st.container(border=True):

        st.subheader("🔌 Appliance Data")

        st.markdown(
            "**Required CSV Columns:**<br>"
            "•&nbsp;"
            "appliance"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•&nbsp;"
            "wattage"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•&nbsp;"
            "hours_per_day"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•&nbsp;"
            "quantity",
            unsafe_allow_html=True
        )
        uploaded_csv = st.file_uploader(
            "Upload Appliance CSV",
            type=["csv"]
        )

        if uploaded_csv is not None:

            try:

                dataframe = pd.read_csv(uploaded_csv)

                required_columns = [
                    "appliance",
                    "wattage",
                    "hours_per_day",
                    "quantity"
                ]

                missing_columns = [
                    column
                    for column in required_columns
                    if column not in dataframe.columns
                ]

                if missing_columns:

                    st.error(
                        "Missing column(s): "
                        + ", ".join(missing_columns)
                    )

                else:

                    dataframe["wattage"] = pd.to_numeric(
                        dataframe["wattage"],
                        errors="raise"
                    )

                    dataframe["hours_per_day"] = pd.to_numeric(
                        dataframe["hours_per_day"],
                        errors="raise"
                    )

                    dataframe["quantity"] = pd.to_numeric(
                        dataframe["quantity"],
                        errors="raise"
                    )

                    st.session_state.appliance_data = dataframe

                    st.success("Appliance data loaded successfully.")

                    st.dataframe(
                        dataframe,
                        use_container_width=True
                    )

                    st.info(
                        f"{len(dataframe)} appliances loaded."
                    )

            except Exception as error:

                st.error(str(error))

        # --------------------------------------------------
        # Sample Appliance Data
        # --------------------------------------------------

        st.markdown("---")

        if st.button("📊 Use Sample Appliance Data"):

            sample_path = os.path.join(
                "data",
                "appliance_data.csv"
            )

            if os.path.exists(sample_path):

                dataframe = pd.read_csv(sample_path)

                st.session_state.appliance_data = dataframe

                st.success("Sample appliance data loaded.")

                st.rerun()

            else:

                st.warning("Sample appliance data not found.")
 
 
# --------------------------------------------------
# Summary
# --------------------------------------------------
 
st.divider()
 
st.header("Data Summary")
 
summary_left, summary_middle, summary_right = st.columns(3)
 
 
with summary_left:
 
    if st.session_state.bill_data:
 
        st.success("Bill Loaded")
 
        st.metric(
            "Metered Units",
            f"{st.session_state.bill_data['metered_units']} kWh"
        )
 
    else:
 
        st.info("No bill uploaded")
 
 
with summary_middle:
 
    if st.session_state.appliance_data is not None:
 
        st.success("Appliances Loaded")
 
        st.metric(
            "Total Appliances",
            len(st.session_state.appliance_data)
        )
 
    else:
 
        st.info("No appliance CSV uploaded")
 
 
with summary_right:
 
    if (
        st.session_state.bill_data
        and st.session_state.appliance_data is not None
    ):
 
        st.success("Ready for Analysis")
 
        if st.button(
            "➡ Go to Analysis",
            type="primary"
        ):
 
            st.switch_page(
                "pages/2_Analysis.py"
            )
 
    else:
 
        st.warning(
            "Upload both the bill and appliance data."
        )
 
 
# --------------------------------------------------
# Instructions
# --------------------------------------------------
 
st.divider()
 
with st.expander("📖 How to Use"):
 
    st.markdown(
        """
### Electricity Bill
 
Upload a PDF electricity bill.
 
The FastAPI backend extracts:
 
- Consumer Number
- Consumer Name
- Bill Month
- Billing Date
- Due Date
- Metered Units
- Total Amount
- Previous Reading
- Current Reading
 
 
### Appliance CSV
 
Required columns:
 
| Column | Example |
|---------|----------|
| appliance | Fan |
| wattage | 75 |
| hours_per_day | 8 |
| quantity | 2 |
 
 
After both datasets are loaded,
continue to the Analysis page.
"""
    )
 
 
# --------------------------------------------------
# CSV Template
# --------------------------------------------------
 
st.divider()
 
st.header("Download CSV Template")
 
template = pd.DataFrame(
    {
        "appliance": [
            "Air Conditioner",
            "Refrigerator",
            "Television"
        ],
        "wattage": [
            1500,
            150,
            100
        ],
        "hours_per_day": [
            8,
            24,
            5
        ],
        "quantity": [
            1,
            1,
            2
        ]
    }
)
 
st.download_button(
    label="📥 Download CSV Template",
    data=template.to_csv(index=False),
    file_name="appliance_template.csv",
    mime="text/csv"
)