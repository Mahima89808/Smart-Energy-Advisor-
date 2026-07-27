"""
Smart Energy Advisor
Streamlit Application Entry Point

Responsibilities:
- Configure the Streamlit application
- Display the landing page
- Introduce the application
- Guide users through navigation

No:
- Database logic
- API logic
- Energy calculations
- Bill extraction
- Suggestion generation
"""

import streamlit as st


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Smart Energy Advisor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# Custom Styling
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title{
        font-size:42px;
        font-weight:bold;
        text-align:center;
        color:#1565C0;
    }

    .subtitle{
        font-size:18px;
        text-align:center;
        color:#555555;
        margin-bottom:25px;
    }

    .feature-box{
        border:1px solid #DDDDDD;
        border-radius:10px;
        padding:18px;
        margin-bottom:15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    "<div class='main-title'>⚡ Smart Energy Advisor</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='subtitle'>
    Analyze electricity consumption, understand appliance energy usage,
    and receive practical energy-saving recommendations.
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# --------------------------------------------------
# Overview
# --------------------------------------------------

st.markdown("## Project Overview")

st.write(
    """
Smart Energy Advisor is an offline-first electricity consumption
analysis application designed to help users understand their
electricity usage and identify opportunities to reduce energy costs.

The application operates completely on your local machine using:

- Streamlit frontend
- FastAPI backend
- SQLite database
- JSON-based knowledge engine

No cloud services, external APIs, or online AI services are required.
"""
)

st.divider()


# --------------------------------------------------
# Features
# --------------------------------------------------

st.markdown("## Features")

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        """
<div class="feature-box">

### 📄 Bill Processing

Current Support

- PDF electricity bill upload

Planned Support

- Image OCR
- CSV import
- Manual bill entry

</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="feature-box">

### ⚡ Energy Analysis

- Daily energy consumption
- Monthly energy consumption
- Appliance running cost
- Bill contribution
- Tariff calculation from uploaded bill

</div>
""",
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
<div class="feature-box">

### 💡 Energy Saving Suggestions

- Appliance recommendations
- Estimated monthly savings
- Estimated yearly savings
- Rule-based knowledge engine

</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="feature-box">

### 📚 Analysis History

- Save completed analyses
- View previous reports
- Maintain historical appliance snapshots

</div>
""",
        unsafe_allow_html=True
    )


st.divider()


# --------------------------------------------------
# Navigation
# --------------------------------------------------

st.markdown("## Application Pages")

st.markdown(
    """
- **Home** – Upload bills and manage appliance information.
- **Analysis** – View electricity consumption analysis.
- **Suggestions** – Review energy-saving recommendations.
- **History** – Access previously saved analyses.
- **About** – Learn more about the project.
"""
)

st.divider()


# --------------------------------------------------
# Workflow
# --------------------------------------------------

st.markdown("## Typical Workflow")

st.markdown(
    """
1. Upload an electricity bill.
2. Add or manage appliance information.
3. Analyze electricity consumption.
4. Review appliance-wise costs.
5. Explore energy-saving suggestions.
6. Save the analysis for future reference.
"""
)

st.divider()


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.caption(
    "Smart Energy Advisor • Offline Electricity Consumption Analysis System"
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("Navigation")

    st.write(
        """
Use the sidebar pages to access:

- Home
- Analysis
- Suggestions
- History
- About
"""
    )

    st.info(
        "Start by opening the Home page and uploading your electricity bill."
    )