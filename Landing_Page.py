"""
Smart Energy Advisor
Streamlit Application Entry Point

Responsibilities:
- Configure the Streamlit application
- Define and route between pages via st.navigation
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

from utils.sidebar import render_sidebar


# --------------------------------------------------
# Landing Page Content
# --------------------------------------------------

def render_landing() -> None:   
    # ensure_session_id()

    st.set_page_config(
        page_title="Smart Energy Advisor",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    render_sidebar()

    # ----------------------------------------
    # Custom Styling
    # ----------------------------------------

    st.markdown(
        """
        <style>

        .main-title{
            font-size:50px;
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
            border:2px solid #DDDDDD;
            border-radius:10px;
            padding:18px;
            margin-bottom:15px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # ----------------------------------------
    # Header
    # ----------------------------------------

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

    # ----------------------------------------
    # Overview
    # ----------------------------------------

    st.markdown("## Overview")

    st.write(
        """
Smart Energy Advisor is an offline-first electricity consumption
analysis application designed to help users understand their
electricity usage and identify opportunities to reduce energy costs.

The application operates completely on your local machine using:

- Streamlit frontend
- FastAPI backend
- Supabase PostgreSQL database
- JSON-based knowledge engine

No cloud services, external APIs, or online AI services are required.
"""
    )

    st.divider()

    # ----------------------------------------
    # Features
    # ----------------------------------------

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

    # ----------------------------------------
    # Navigation
    # ----------------------------------------

    st.markdown("## Application Pages")

    with st.container(border=True):

        st.markdown(
            "**Home** – Upload bills and manage appliance information."
        )
        st.markdown(
            "**Analysis** – View electricity consumption analysis."
        )
        st.markdown(
            "**Suggestions** – Review energy-saving recommendations."
        )
        st.markdown(
            "**History** – Access previously saved analyses."
        )
        st.markdown(
            "**About** – Learn more about the project."
        )

    st.divider()

    # ----------------------------------------
    # Workflow
    # ----------------------------------------

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

    # ----------------------------------------
    # Footer
    # ----------------------------------------

    st.caption(
        "Smart Energy Advisor • Offline Electricity Consumption Analysis System"
    )


# --------------------------------------------------
# Page Declarations + Navigation
# --------------------------------------------------

landing_page = st.Page(
    render_landing,
    title="Landing Page",
    icon="⚡",
    default=True
)

home_page = st.Page(
    "pages/1_Home.py",
    title="Home",
    icon="🏠"
)

analysis_page = st.Page(
    "pages/2_Analysis.py",
    title="Analysis",
    icon="📊"
)

suggestions_page = st.Page(
    "pages/3_Suggestions.py",
    title="Suggestions",
    icon="💡"
)

history_page = st.Page(
    "pages/4_History.py",
    title="History",
    icon="📚"
)

about_page = st.Page(
    "_About.py",
    title="About",
    icon="ℹ️",
    visibility="hidden"
)

nav = st.navigation(
    [
        landing_page,
        home_page,
        analysis_page,
        suggestions_page,
        history_page,
        about_page
    ]
)

nav.run()