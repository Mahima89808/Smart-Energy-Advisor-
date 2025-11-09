"""
Home Page - Smart AI Energy Advisor System
Handles file uploads (PDF bills and CSV appliance data) and data extraction.
"""

import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.extract_data import extract_bill_data, extract_text_from_pdf

# Page configuration
st.set_page_config(page_title="Home - Energy Advisor", page_icon="🏠", layout="wide")

st.title("🏠 Home - Upload & Extract Data")
st.markdown("Upload your electricity bill and appliance usage data to begin analysis")

st.divider()

# Initialize session state
if 'bill_data' not in st.session_state:
    st.session_state.bill_data = None
if 'appliance_data' not in st.session_state:
    st.session_state.appliance_data = None
if 'raw_bill_text' not in st.session_state:
    st.session_state.raw_bill_text = None

# Two column layout
col1, col2 = st.columns(2)

# Left column - Bill Upload
with col1:
    st.markdown("### 📄 Upload Electricity Bill")
    st.markdown("Upload your electricity bill in PDF format for automatic data extraction")
    
    uploaded_bill = st.file_uploader(
        "Choose your electricity bill (PDF)",
        type=['pdf'],
        help="Upload a PDF of your electricity bill"
    )
    
    if uploaded_bill is not None:
        with st.spinner("Extracting data from bill..."):
            # Extract data
            bill_data = extract_bill_data(uploaded_bill)
            
            # Rewind the file stream for second extraction
            uploaded_bill.seek(0)
            raw_text = extract_text_from_pdf(uploaded_bill)
            
            # Store in session state
            st.session_state.bill_data = bill_data
            st.session_state.raw_bill_text = raw_text
            
        st.success("✅ Bill uploaded and processed successfully!")
        
        # Display extracted information
        st.markdown("#### 📋 Extracted Bill Information")
        
        info_col1, info_col2 = st.columns(2)
        
        with info_col1:
            st.metric("Consumer Number", bill_data['consumer_no'])
            st.metric("Consumer Name", bill_data['consumer_name'])
            st.metric("Bill Month", bill_data['bill_month'])
            st.metric("Billing Date", bill_data['billing_date'])
        
        with info_col2:
            st.metric("Due Date", bill_data['due_date'])
            st.metric("Metered Units (kWh)", f"{bill_data['metered_units']:.2f}")
            st.metric("Total Amount", f"₹{bill_data['total_amount']:.2f}")
            st.metric("Previous Reading", bill_data['previous_reading'])
        
        # Show raw text in expander
        with st.expander("🔍 View Raw Extracted Text"):
            st.text(raw_text)
    else:
        st.info("👆 Upload your electricity bill to extract consumption data")
        
        # Option to use sample bill
        if st.button("📝 Use Sample Bill"):
            sample_path = os.path.join('data', 'sample_bill.txt')
            if os.path.exists(sample_path):
                with open(sample_path, 'r') as f:
                    sample_text = f.read()
                
                # Mock extraction for sample text file
                st.session_state.bill_data = {
                    'consumer_no': '1234567890',
                    'consumer_name': 'JOHN DOE',
                    'bill_month': 'October 2024',
                    'billing_date': '01/11/2024',
                    'due_date': '15/11/2024',
                    'metered_units': 400,
                    'total_amount': 3152.50,
                    'previous_reading': 8450,
                    'current_reading': 8850
                }
                st.session_state.raw_bill_text = sample_text
                st.rerun()
            else:
                st.warning("Sample bill file not found")

# Right column - Appliance Data Upload
with col2:
    st.markdown("### 🔌 Upload Appliance Usage Data")
    st.markdown("Upload a CSV file with your appliance usage details")
    
    st.markdown("""
    **Required CSV Format:**
    - `appliance`: Name of appliance
    - `wattage`: Power consumption in watts
    - `hours_per_day`: Average daily usage hours
    - `quantity`: Number of units
    """)
    
    uploaded_appliances = st.file_uploader(
        "Choose appliance data file (CSV)",
        type=['csv'],
        help="Upload a CSV file with appliance information"
    )
    
    if uploaded_appliances is not None:
        try:
            df = pd.read_csv(uploaded_appliances)
            
            # Validate required columns
            required_cols = ['appliance', 'wattage', 'hours_per_day', 'quantity']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if not missing_cols:
                # Additional validation for numeric columns
                try:
                    df['wattage'] = pd.to_numeric(df['wattage'], errors='raise')
                    df['hours_per_day'] = pd.to_numeric(df['hours_per_day'], errors='raise')
                    df['quantity'] = pd.to_numeric(df['quantity'], errors='raise')
                    
                    st.session_state.appliance_data = df
                    st.success("✅ Appliance data uploaded successfully!")
                    
                    st.markdown("#### 📊 Uploaded Appliance Data")
                    st.dataframe(df, use_container_width=True)
                    
                    st.info(f"Total appliances: {len(df)}")
                except ValueError as ve:
                    st.error(f"❌ Error: Numeric columns (wattage, hours_per_day, quantity) must contain valid numbers. {str(ve)}")
            else:
                st.error(f"❌ CSV is missing required column(s): {', '.join(missing_cols)}. Required columns are: {', '.join(required_cols)}")
                
        except Exception as e:
            st.error(f"❌ Error reading CSV file: {str(e)}")
    else:
        st.info("👆 Upload your appliance usage data in CSV format")
        
        # Option to use sample data
        if st.button("📊 Use Sample Appliance Data"):
            sample_path = os.path.join('data', 'appliance_data.csv')
            if os.path.exists(sample_path):
                df = pd.read_csv(sample_path)
                st.session_state.appliance_data = df
                st.rerun()
            else:
                st.warning("Sample appliance data file not found")

st.divider()

# Summary section
st.markdown("### 📌 Data Summary")

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    if st.session_state.bill_data:
        st.success("✅ Bill Data Loaded")
        st.metric("Total Units", f"{st.session_state.bill_data['metered_units']} kWh")
    else:
        st.warning("⏳ No bill data uploaded")

with summary_col2:
    if st.session_state.appliance_data is not None:
        st.success("✅ Appliance Data Loaded")
        st.metric("Total Appliances", len(st.session_state.appliance_data))
    else:
        st.warning("⏳ No appliance data uploaded")

with summary_col3:
    if st.session_state.bill_data and st.session_state.appliance_data is not None:
        st.success("✅ Ready for Analysis")
        if st.button("📊 Go to Analysis →", type="primary"):
            st.switch_page("pages/2_Analysis.py")
    else:
        st.info("ℹ️ Upload both files to proceed")

st.divider()

# Instructions
with st.expander("📖 How to prepare your data"):
    st.markdown("""
    ### Electricity Bill (PDF)
    - Upload your latest electricity bill in PDF format
    - The system will automatically extract key information
    - Supported information: Consumer details, billing period, units consumed, amount
    
    ### Appliance Data (CSV)
    Create a CSV file with the following columns:
    
    | Column | Description | Example |
    |--------|-------------|---------|
    | appliance | Name of the appliance | Air Conditioner |
    | wattage | Power consumption in watts | 1500 |
    | hours_per_day | Average daily usage | 8 |
    | quantity | Number of units | 2 |
    
    ### Sample Data
    Click the "Use Sample" buttons to explore the system with pre-loaded data.
    """)

# Download sample CSV template
st.divider()
st.markdown("### 📥 Download Template")

template_df = pd.DataFrame({
    'appliance': ['Air Conditioner', 'Refrigerator', 'Television'],
    'wattage': [1500, 150, 100],
    'hours_per_day': [8, 24, 5],
    'quantity': [1, 1, 2]
})

csv = template_df.to_csv(index=False)
st.download_button(
    label="📥 Download CSV Template",
    data=csv,
    file_name="appliance_data_template.csv",
    mime="text/csv",
    help="Download a template CSV file to fill with your appliance data"
)
