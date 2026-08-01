"""
Home Page
Smart Energy Advisor

Responsibilities:
- Upload electricity bills (PDF / CSV / Manual)
- Manage appliance data (upload CSV, add/edit/delete, load previous list)
- Call FastAPI through api_client
- Store extracted data in Streamlit session

No:
- PDF extraction logic
- Database logic
- Business logic
"""

import pandas as pd
import requests
import streamlit as st

from utils.api_client import (
    extract_bill_pdf,
    extract_bill_csv,
    extract_bill_manual,
    get_appliances,
    create_appliance,
    update_appliance,
    delete_appliance,
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
session_id = st.session_state.session_id

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

if "appliance_editor_version" not in st.session_state:
    st.session_state.appliance_editor_version = 0

if "last_processed_bill_pdf" not in st.session_state:
    st.session_state.last_processed_bill_pdf = None

if "last_processed_bill_csv" not in st.session_state:
    st.session_state.last_processed_bill_csv = None


BILL_CSV_COLUMNS = [
    "consumer_no",
    "consumer_name",
    "bill_month",
    "billing_date",
    "due_date",
    "metered_units",
    "total_amount",
    "previous_reading",
    "current_reading",
]

APPLIANCE_COLUMNS = ["id", "name", "category", "wattage", "hours_per_day", "quantity"]


def _connection_error_message():
    st.error(
        "Cannot connect to the backend.\n\n"
        "Start FastAPI using:\n\n"
        "uvicorn backend.main:app --reload"
    )


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
            ["PDF", "CSV", "Manual"],
            horizontal=True
        )

        # ----------------------------------------------------
        # PDF
        # ----------------------------------------------------
        if bill_input_method == "PDF":

            uploaded_bill = st.file_uploader(
                "Upload PDF Bill",
                type=["pdf"],
                key="pdf_bill",
            )
            if uploaded_bill is not None:
                file_signature = getattr(uploaded_bill, "file_id", None) or f"{uploaded_bill.name}-{uploaded_bill.size}"

                if st.session_state.last_processed_bill_pdf != file_signature:
                    try:
                        with st.spinner("Extracting bill data..."):
                            st.session_state.bill_data = extract_bill_pdf(uploaded_bill)
                        st.session_state.last_processed_bill_pdf = file_signature
                        st.success("Bill extracted successfully.")
                    except requests.ConnectionError:
                        _connection_error_message()
                    except Exception as error:
                        st.error(str(error))
                else:
                    st.success("Bill extracted successfully.")

        # ----------------------------------------------------
        # CSV
        # ----------------------------------------------------
        elif bill_input_method == "CSV":

            st.caption("Expected columns (any subset works, missing ones default to N/A / 0):")
            st.code(", ".join(BILL_CSV_COLUMNS), language=None)

            template_df = pd.DataFrame([{col: "" for col in BILL_CSV_COLUMNS}])
            st.download_button(
                "📥 Download Bill CSV Template",
                data=template_df.to_csv(index=False),
                file_name="bill_template.csv",
                mime="text/csv",
            )

            if uploaded_bill is not None:
                file_signature = getattr(uploaded_bill, "file_id", None) or f"{uploaded_bill.name}-{uploaded_bill.size}"

                if st.session_state.last_processed_bill_csv != file_signature:
                    try:
                        preview_df = pd.read_csv(uploaded_bill)
                        uploaded_bill.seek(0)

                        matched = [c for c in BILL_CSV_COLUMNS if c in preview_df.columns]
                        missing = [c for c in BILL_CSV_COLUMNS if c not in preview_df.columns]

                        if not matched:
                            st.error(
                                "None of the expected columns were found in this CSV.\n\n"
                                f"Found columns: {', '.join(preview_df.columns)}\n\n"
                                f"Expected (any subset): {', '.join(BILL_CSV_COLUMNS)}"
                            )
                        else:
                            if missing:
                                st.info(f"These columns are missing and will default: {', '.join(missing)}")

                            with st.spinner("Extracting bill data..."):
                                st.session_state.bill_data = extract_bill_csv(uploaded_bill)
                            st.session_state.last_processed_bill_csv = file_signature
                            st.success("Bill extracted successfully.")

                    except requests.ConnectionError:
                        _connection_error_message()
                    except Exception as error:
                        st.error(str(error))
                else:
                    st.success("Bill extracted successfully.")

        # ----------------------------------------------------
        # Manual
        # ----------------------------------------------------
        else:

            with st.form("manual_bill_form"):

                form_left, form_right = st.columns(2)

                with form_left:
                    consumer_no = st.text_input("Consumer Number")
                    consumer_name = st.text_input("Consumer Name")
                    bill_month = st.text_input("Bill Month (e.g. JAN-2026)")
                    billing_date = st.text_input("Billing Date (DD/MM/YYYY)")
                    due_date = st.text_input("Due Date (DD/MM/YYYY)")

                with form_right:
                    metered_units = st.number_input("Metered Units (kWh)", min_value=0.0, step=1.0)
                    total_amount = st.number_input("Total Amount (₹)", min_value=0.0, step=1.0)
                    previous_reading = st.number_input("Previous Reading", min_value=0.0, step=1.0)
                    current_reading = st.number_input("Current Reading", min_value=0.0, step=1.0)

                submitted = st.form_submit_button("Save Bill Data", type="primary")

            if submitted:
                manual_entry = {
                    "consumer_no": consumer_no or None,
                    "consumer_name": consumer_name or None,
                    "bill_month": bill_month or None,
                    "billing_date": billing_date or None,
                    "due_date": due_date or None,
                    "metered_units": metered_units or None,
                    "total_amount": total_amount or None,
                    "previous_reading": previous_reading or None,
                    "current_reading": current_reading or None,
                }

                with st.expander("🔍 Debug: values submitted", expanded=False):
                    st.json(manual_entry)

                if manual_entry["total_amount"] is None:
                    st.warning(
                        "Total Amount was 0 or empty, so it was not sent — "
                        "it will show as ₹0.00. Re-check the field above and re-submit if needed."
                    )

                try:
                    with st.spinner("Saving bill data..."):
                        st.session_state.bill_data = extract_bill_manual(manual_entry)
                    st.success("Bill data saved successfully.")
                except requests.ConnectionError:
                    _connection_error_message()
                except Exception as error:
                    st.error(str(error))

        # ----------------------------------------------------
        # Extracted Bill Display
        # ----------------------------------------------------
        if st.session_state.bill_data:

            bill = st.session_state.bill_data

            st.markdown("### Extracted Bill Information")

            info_left, info_right = st.columns(2)

            with info_left:
                st.metric("Consumer Number", bill["consumer_no"])
                st.metric("Consumer Name", bill["consumer_name"])
                st.metric("Bill Month", bill["bill_month"])
                st.metric("Billing Date", bill["billing_date"])

            with info_right:
                st.metric("Due Date", bill["due_date"])
                st.metric("Metered Units", f"{bill['metered_units']:.2f} kWh")
                st.metric("Total Amount", f"₹{bill['total_amount']:.2f}")
                st.metric("Previous Reading", bill["previous_reading"])
                st.metric("Current Reading", bill["current_reading"])


# ==================================================
# RIGHT COLUMN
# Appliance Data (Upload / Previous List / Add / Edit / Delete)
# ==================================================

with right_column:

    with st.container(border=True):

        st.subheader("🔌 Appliance Data")

        st.markdown(
            "**CSV Columns:**<br>"
            "•&nbsp;name (or appliance)&nbsp;&nbsp;&nbsp;"
            "•&nbsp;wattage&nbsp;&nbsp;&nbsp;"
            "•&nbsp;hours_per_day&nbsp;&nbsp;&nbsp;"
            "•&nbsp;quantity&nbsp;&nbsp;&nbsp;"
            "•&nbsp;category (optional)",
            unsafe_allow_html=True
        )

        upload_col, prev_col = st.columns(2)

        with upload_col:
            uploaded_csv = st.file_uploader(
                "Upload Appliance CSV",
                type=["csv"],
                key="appliance_csv"
            )

        with prev_col:
            st.write("")
            st.write("")
            if st.button("📋 Previous Appliances List", use_container_width=True):
                try:
                    saved_appliances = get_appliances(session_id)
                    if saved_appliances:
                        st.session_state.appliance_data = pd.DataFrame(saved_appliances)[APPLIANCE_COLUMNS]
                        st.success(f"Loaded {len(saved_appliances)} saved appliance(s).")
                    else:
                        st.session_state.appliance_data = pd.DataFrame(columns=APPLIANCE_COLUMNS)
                        st.info("No previously saved appliances yet. Add rows below and click Save.")
                    st.session_state.appliance_editor_version += 1
                    st.rerun()
                except requests.ConnectionError:
                    _connection_error_message()
                except Exception as error:
                    st.error(str(error))

        if uploaded_csv is not None:
            file_signature = getattr(uploaded_csv, "file_id", None) or f"{uploaded_csv.name}-{uploaded_csv.size}"

            if st.session_state.get("last_processed_appliance_csv") != file_signature:
                try:
                    dataframe = pd.read_csv(uploaded_csv)

                    if "appliance" in dataframe.columns and "name" not in dataframe.columns:
                        dataframe = dataframe.rename(columns={"appliance": "name"})

                    if "category" not in dataframe.columns:
                        dataframe["category"] = "General"

                    required_columns = ["name", "wattage", "hours_per_day", "quantity"]
                    missing_columns = [c for c in required_columns if c not in dataframe.columns]

                    if missing_columns:
                        st.error("Missing column(s): " + ", ".join(missing_columns))
                    else:
                        dataframe["wattage"] = pd.to_numeric(dataframe["wattage"], errors="raise")
                        dataframe["hours_per_day"] = pd.to_numeric(dataframe["hours_per_day"], errors="raise")
                        dataframe["quantity"] = pd.to_numeric(dataframe["quantity"], errors="raise")

                        if "id" not in dataframe.columns:
                            dataframe["id"] = None

                        dataframe = dataframe[APPLIANCE_COLUMNS]

                        st.session_state.appliance_data = dataframe
                        st.session_state.appliance_editor_version += 1
                        st.session_state["last_processed_appliance_csv"] = file_signature
                        st.success(f"{len(dataframe)} appliance(s) loaded from CSV. Click Save below to store them.")

                except Exception as error:
                    st.error(str(error))

        st.markdown("---")

        if st.session_state.appliance_data is None:
            st.session_state.appliance_data = pd.DataFrame(columns=APPLIANCE_COLUMNS)

        st.markdown("**Appliance List** — add, edit, or delete rows, then click Save.")

        original_appliance_df = st.session_state.appliance_data.copy()

        edited_df = st.data_editor(
            original_appliance_df,
            num_rows="dynamic",
            use_container_width=True,
            key=f"appliance_editor_{st.session_state.appliance_editor_version}",
            column_config={
                "id": st.column_config.NumberColumn("ID", disabled=True),
                "name": st.column_config.TextColumn("Appliance Name", required=True),
                "category": st.column_config.TextColumn("Category"),
                "wattage": st.column_config.NumberColumn("Wattage (W)", min_value=0.0, required=True),
                "hours_per_day": st.column_config.NumberColumn("Hours/Day", min_value=0.0, max_value=24.0, required=True),
                "quantity": st.column_config.NumberColumn("Quantity", min_value=1, step=1, required=True),
            }
        )

        st.session_state.appliance_data = edited_df

        if st.button("💾 Save Appliance List", type="primary"):
            try:
                backend_appliances = get_appliances(session_id)
                backend_ids = {a["id"] for a in backend_appliances}

                edited_ids = set(
                    pd.to_numeric(edited_df["id"], errors="coerce").dropna().astype(int)
                ) if "id" in edited_df.columns else set()

                removed_ids = backend_ids - edited_ids

                for appliance_id in removed_ids:
                    delete_appliance(session_id, appliance_id)

                saved_count = 0

                for _, row in edited_df.iterrows():

                    name = str(row.get("name") or "").strip()
                    if not name:
                        continue

                    if pd.isna(row.get("wattage")) or pd.isna(row.get("hours_per_day")) or pd.isna(row.get("quantity")):
                        st.warning(f"Skipped '{name}' — wattage/hours_per_day/quantity is required.")
                        continue

                    payload = {
                        "name": name,
                        "category": str(row.get("category") or "General").strip() or "General",
                        "wattage": float(row["wattage"]),
                        "hours_per_day": float(row["hours_per_day"]),
                        "quantity": int(row["quantity"]),
                    }

                    row_id = row.get("id")

                    if pd.notna(row_id) and int(row_id) in backend_ids:
                        update_appliance(session_id, int(row_id), payload)
                    else:
                        create_appliance(session_id, payload)

                    saved_count += 1

                st.success(f"Saved. {saved_count} appliance(s) in list, {len(removed_ids)} removed.")

                st.session_state.appliance_data = pd.DataFrame(get_appliances(session_id))[APPLIANCE_COLUMNS]
                st.session_state.appliance_editor_version += 1
                st.rerun()

            except requests.ConnectionError:
                _connection_error_message()
            except Exception as error:
                st.error(str(error))

# --------------------------------------------------
# Summary
# --------------------------------------------------

st.divider()

st.header("Data Summary")

summary_left, summary_middle, summary_right = st.columns(3)

with summary_left:
    if st.session_state.bill_data:
        st.success("Bill Loaded")
        st.metric("Metered Units", f"{st.session_state.bill_data['metered_units']} kWh")
    else:
        st.info("No bill uploaded")

with summary_middle:
    if st.session_state.appliance_data is not None and len(st.session_state.appliance_data) > 0:
        st.success("Appliances Loaded")
        st.metric("Total Appliances", len(st.session_state.appliance_data))
    else:
        st.info("No appliance data")

with summary_right:
    has_appliances = (
        st.session_state.appliance_data is not None
        and len(st.session_state.appliance_data) > 0
    )
    if st.session_state.bill_data and has_appliances:
        st.success("Ready for Analysis")
        if st.button("➡ Go to Analysis", type="primary"):
            st.switch_page("pages/2_Analysis.py")
    else:
        st.warning("Upload both the bill and appliance data.")


# --------------------------------------------------
# Instructions
# --------------------------------------------------

st.divider()

with st.expander("📖 How to Use"):
    st.markdown(
        """
### Electricity Bill

Choose PDF, CSV, or Manual entry.

- **PDF**: upload a scanned/text electricity bill PDF.
- **CSV**: upload a single-row CSV with the expected column headers.
- **Manual**: fill in the form fields directly.

### Appliance Data

- Upload a CSV, or click **Previous Appliances List** to load what's saved in the database.
- Edit the table directly — add new rows, change values, or delete rows.
- Click **Save Appliance List** to persist your changes to the database.

After both a bill and appliances are loaded, continue to the Analysis page.
"""
    )


# --------------------------------------------------
# Appliance CSV Template
# --------------------------------------------------

st.divider()

st.header("Download Appliance CSV Template")

template = pd.DataFrame(
    {
        "name": ["Air Conditioner", "Refrigerator", "Television"],
        "category": ["Cooling", "Kitchen", "Entertainment"],
        "wattage": [1500, 150, 100],
        "hours_per_day": [8, 24, 5],
        "quantity": [1, 1, 2],
    }
)

st.download_button(
    label="📥 Download Appliance CSV Template",
    data=template.to_csv(index=False),
    file_name="appliance_template.csv",
    mime="text/csv"
)