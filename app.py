"""
Smart AI Energy Advisor System
Main entry point for the Streamlit multi-page application.
Provides navigation and welcome interface for the energy analysis platform.
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Smart AI Energy Advisor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #424242;
        margin-bottom: 2rem;
    }
    .feature-box {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f5f5f5;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Main page content
st.markdown('<div class="main-header">⚡ Smart AI Energy Advisor System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Analyze your energy consumption and get AI-powered recommendations to save energy and money</div>', unsafe_allow_html=True)

st.divider()

# Welcome section
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🏠 Home")
    st.markdown("""
    <div class="feature-box">
    Upload your electricity bill and appliance data to get started with comprehensive energy analysis.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### 📊 Analysis")
    st.markdown("""
    <div class="feature-box">
    View detailed analysis of your energy consumption patterns with interactive charts and insights.
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("### 💡 Suggestions")
    st.markdown("""
    <div class="feature-box">
    Get AI-powered energy-saving recommendations tailored to your consumption patterns.
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Key features
st.markdown("## 🌟 Key Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 📄 Bill Analysis
    - Extract data from PDF electricity bills
    - Automatic parsing of key information
    - Consumer details and billing summary
    
    #### 📈 Consumption Insights
    - Appliance-wise energy breakdown
    - Interactive visualizations
    - Cost analysis and projections
    """)

with col2:
    st.markdown("""
    #### 🤖 AI Recommendations
    - Personalized energy-saving tips
    - Identify energy-hungry appliances
    - Calculate potential savings
    
    #### 💰 Cost Optimization
    - Monthly and annual cost projections
    - Efficiency score calculation
    - Savings potential analysis
    """)

st.divider()

# How it works
st.markdown("## 🚀 How It Works")

steps_col1, steps_col2, steps_col3, steps_col4 = st.columns(4)

with steps_col1:
    st.markdown("""
    **Step 1: Upload**
    
    Upload your electricity bill (PDF) and appliance usage data (CSV)
    """)

with steps_col2:
    st.markdown("""
    **Step 2: Extract**
    
    AI extracts key information from your bill automatically
    """)

with steps_col3:
    st.markdown("""
    **Step 3: Analyze**
    
    View detailed analysis with interactive charts and insights
    """)

with steps_col4:
    st.markdown("""
    **Step 4: Optimize**
    
    Get personalized recommendations to reduce energy consumption
    """)

st.divider()

# Quick start guide
st.markdown("## 📖 Quick Start Guide")

with st.expander("👉 Click here to see the quick start guide"):
    st.markdown("""
    1. **Go to Home Page**: Navigate to the Home page from the sidebar
    2. **Upload Bill**: Upload your electricity bill in PDF format
    3. **Upload Appliance Data**: Upload your appliance usage data in CSV format (or use sample data)
    4. **View Analysis**: Go to the Analysis page to see detailed consumption insights
    5. **Get Suggestions**: Visit the Suggestions page for AI-powered energy-saving recommendations
    
    ### Sample Data Available
    The system comes with sample data to help you explore features:
    - Sample electricity bill
    - Sample appliance usage data
    
    You can use these to understand how the system works before uploading your own data.
    """)

st.divider()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #757575;'>
    <p>Smart AI Energy Advisor System | Powered by AI & Machine Learning</p>
    <p>Start your journey towards energy efficiency today! 💚</p>
</div>
""", unsafe_allow_html=True)

# Sidebar information
with st.sidebar:
    st.markdown("## 🎯 Navigation")
    st.markdown("""
    Use the navigation menu to explore:
    - **Home**: Upload and extract data
    - **Analysis**: View consumption insights
    - **Suggestions**: Get recommendations
    - **About**: Learn more about the system
    """)
    
    st.divider()
    
    st.markdown("## 💡 Quick Tip")
    st.info("Upload your electricity bill and appliance data on the Home page to get started!")
