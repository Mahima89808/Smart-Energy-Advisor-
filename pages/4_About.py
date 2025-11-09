"""
About Page - Smart AI Energy Advisor System
Information about the system, features, technology stack, and usage guide.
"""

import streamlit as st

# Page configuration
st.set_page_config(page_title="About - Energy Advisor", page_icon="ℹ️", layout="wide")

st.title("ℹ️ About Smart AI Energy Advisor System")
st.markdown("Learn more about how this system helps you save energy and money")

st.divider()

# Introduction
st.markdown("## 🎯 What is Smart AI Energy Advisor?")

st.markdown("""
The **Smart AI Energy Advisor System** is an intelligent, AI-powered web application designed to help 
households and businesses analyze their energy consumption patterns and receive personalized recommendations 
for reducing energy usage and costs.

By combining advanced data extraction, statistical analysis, and machine learning techniques, this system 
provides actionable insights that can help you:

- 📊 Understand your energy consumption patterns
- 💰 Identify opportunities to save money
- 🌍 Reduce your carbon footprint
- 🎯 Make informed decisions about energy usage
""")

st.divider()

# Key Features
st.markdown("## ⭐ Key Features")

features_col1, features_col2 = st.columns(2)

with features_col1:
    st.markdown("""
    ### 📄 Bill Analysis
    - **PDF Data Extraction**: Automatically extract key information from electricity bills
    - **Smart Parsing**: Uses advanced regex patterns to identify consumer details, billing dates, and charges
    - **Multi-format Support**: Handles various bill formats and layouts
    
    ### 📊 Consumption Analysis
    - **Appliance-wise Breakdown**: Detailed analysis of each appliance's energy consumption
    - **Interactive Visualizations**: Beautiful charts using Plotly for better insights
    - **Cost Calculations**: Automatic calculation of daily, monthly, and annual costs
    - **Category Classification**: Appliances grouped by consumption levels
    """)

with features_col2:
    st.markdown("""
    ### 💡 AI Recommendations
    - **Personalized Suggestions**: Tailored recommendations based on your usage patterns
    - **Energy Hog Detection**: Identify appliances consuming excessive energy
    - **Savings Projections**: Calculate potential savings from efficiency improvements
    - **Action Plans**: Step-by-step guide to reduce consumption
    
    ### 📈 Advanced Analytics
    - **Efficiency Scoring**: Overall energy efficiency rating
    - **Trend Analysis**: Understand consumption patterns over time
    - **Comparative Analysis**: Compare calculated vs actual consumption
    - **Environmental Impact**: Track your carbon footprint reduction
    """)

st.divider()

# Technology Stack
st.markdown("## 🛠️ Technology Stack")

tech_col1, tech_col2, tech_col3 = st.columns(3)

with tech_col1:
    st.markdown("""
    ### Frontend
    - **Streamlit**: Interactive web interface
    - **Plotly**: Data visualization
    - **Custom CSS**: Enhanced UI/UX
    """)

with tech_col2:
    st.markdown("""
    ### Data Processing
    - **Pandas**: Data manipulation
    - **NumPy**: Numerical computations
    - **PDFPlumber**: PDF text extraction
    - **Pytesseract**: OCR capabilities
    """)

with tech_col3:
    st.markdown("""
    ### AI & Analytics
    - **Scikit-learn**: Pattern analysis
    - **Statistical Models**: Consumption prediction
    - **Regex**: Smart data extraction
    """)

st.divider()

# How It Works
st.markdown("## 🔄 How It Works")

workflow_tabs = st.tabs(["1️⃣ Data Collection", "2️⃣ Processing", "3️⃣ Analysis", "4️⃣ Recommendations"])

with workflow_tabs[0]:
    st.markdown("""
    ### 📥 Data Collection
    
    The system collects two types of data:
    
    **1. Electricity Bill (PDF)**
    - Upload your electricity bill in PDF format
    - System extracts text using PDFPlumber
    - Regex patterns identify key information:
        - Consumer number and name
        - Billing period and dates
        - Meter readings
        - Units consumed
        - Total charges
    
    **2. Appliance Usage Data (CSV)**
    - Create or upload a CSV file with appliance details:
        - Appliance name
        - Power rating (watts)
        - Daily usage hours
        - Quantity
    - System validates and processes the data
    """)

with workflow_tabs[1]:
    st.markdown("""
    ### ⚙️ Data Processing
    
    **Consumption Calculation**
    ```
    Daily Consumption (kWh) = (Wattage × Hours × Quantity) / 1000
    Monthly Consumption (kWh) = Daily Consumption × 30
    Monthly Cost (₹) = Monthly Consumption × Rate per kWh
    ```
    
    **Energy Classification**
    - **Low**: < 10 kWh/month
    - **Medium**: 10-50 kWh/month
    - **High**: 50-150 kWh/month
    - **Very High**: > 150 kWh/month
    
    **Efficiency Scoring**
    - Analyzes consumption distribution
    - Calculates coefficient of variation
    - Compares with actual bill (if available)
    - Generates 0-100 efficiency score
    """)

with workflow_tabs[2]:
    st.markdown("""
    ### 📊 Analysis & Insights
    
    **Statistical Analysis**
    - Total and average consumption
    - Peak consumption identification
    - Cost distribution analysis
    - Consumption variance calculation
    
    **Visual Analysis**
    - Pie charts for distribution
    - Bar charts for comparisons
    - Category breakdowns
    - Trend visualizations
    
    **Pattern Recognition**
    - Identify energy hogs (>10% consumption)
    - Detect imbalanced usage
    - Compare calculated vs actual consumption
    - Highlight anomalies
    """)

with workflow_tabs[3]:
    st.markdown("""
    ### 💡 AI-Powered Recommendations
    
    **Smart Suggestions**
    - Appliance-specific recommendations
    - Based on consumption patterns
    - Prioritized by impact
    - Actionable and practical
    
    **Savings Calculator**
    - Set target reduction percentage
    - Calculate potential savings
    - Project annual impact
    - Environmental benefits
    
    **Action Plans**
    - Immediate actions (this week)
    - Short-term goals (this month)
    - Long-term plans (3-6 months)
    - Investment recommendations
    """)

st.divider()

# User Guide
st.markdown("## 📖 User Guide")

with st.expander("🚀 Getting Started"):
    st.markdown("""
    1. Navigate to the **Home** page
    2. Upload your electricity bill (PDF) or use the sample bill
    3. Upload your appliance data (CSV) or use the sample data
    4. Review the extracted information
    5. Proceed to **Analysis** to view detailed insights
    6. Visit **Suggestions** for personalized recommendations
    """)

with st.expander("📄 Preparing Your Data"):
    st.markdown("""
    **Electricity Bill:**
    - Must be in PDF format
    - Should contain clear text (not scanned images for best results)
    - Include standard billing information
    
    **Appliance Data CSV:**
    - Required columns: appliance, wattage, hours_per_day, quantity
    - Wattage in watts (e.g., 1500 for 1.5kW)
    - Hours as decimal (e.g., 0.5 for 30 minutes)
    - Quantity as whole numbers
    
    Download the CSV template from the Home page to get started!
    """)

with st.expander("💡 Tips for Best Results"):
    st.markdown("""
    - **Accurate Data**: Provide realistic usage hours for better analysis
    - **Regular Updates**: Update your data monthly to track progress
    - **Bill Comparison**: Upload actual bills to verify calculation accuracy
    - **Complete Inventory**: Include all appliances for comprehensive analysis
    - **Seasonal Adjustments**: Update usage patterns for different seasons
    """)

with st.expander("🔧 Troubleshooting"):
    st.markdown("""
    **Issue: PDF extraction not working**
    - Ensure PDF contains text (not just scanned images)
    - Try using the sample bill to test the system
    - Check PDF is not password protected
    
    **Issue: CSV upload fails**
    - Verify all required columns are present
    - Check for spelling errors in column names
    - Ensure numeric values don't have text
    
    **Issue: Analysis shows unexpected results**
    - Verify appliance wattage values are correct
    - Check hours_per_day are realistic
    - Confirm quantity values are accurate
    """)

st.divider()

# Benefits
st.markdown("## 🌟 Benefits")

benefits_col1, benefits_col2 = st.columns(2)

with benefits_col1:
    st.markdown("""
    ### 💰 Financial Benefits
    - Reduce electricity bills by 15-30%
    - Identify wasteful appliances
    - Optimize usage patterns
    - Plan smart investments in efficient appliances
    - Track savings over time
    """)

with benefits_col2:
    st.markdown("""
    ### 🌍 Environmental Benefits
    - Reduce carbon footprint
    - Lower CO₂ emissions
    - Contribute to climate change mitigation
    - Promote sustainable living
    - Set example for others
    """)

st.divider()

# Future Enhancements
st.markdown("## 🚀 Future Enhancements")

st.markdown("""
We're continuously working to improve the Smart AI Energy Advisor System. Here are some planned features:

- 🔮 **Predictive Analytics**: Forecast future consumption using ML models
- 📱 **Mobile App**: Access insights on the go
- 🔔 **Smart Alerts**: Get notified about unusual consumption spikes
- 📅 **Historical Tracking**: Track consumption trends over months/years
- 🌤️ **Weather Integration**: Correlate consumption with weather patterns
- 🏆 **Gamification**: Earn badges for energy-saving achievements
- 👥 **Community Features**: Compare with similar households
- 🔌 **IoT Integration**: Connect with smart meters for real-time data
- 💡 **Appliance Database**: Pre-filled database of common appliances
- 📊 **Custom Reports**: Generate detailed PDF reports
""")

st.divider()

# FAQs
st.markdown("## ❓ Frequently Asked Questions")

with st.expander("Is my data secure?"):
    st.markdown("""
    Yes! All data processing happens locally in your browser session. 
    No data is stored permanently or sent to external servers.
    Session data is cleared when you close the browser.
    """)

with st.expander("Can I use this for commercial purposes?"):
    st.markdown("""
    Yes! The system works for both residential and commercial applications.
    Just ensure your appliance data is comprehensive for best results.
    """)

with st.expander("How accurate are the calculations?"):
    st.markdown("""
    Calculations are based on standard electrical formulas and are highly accurate.
    However, actual consumption may vary based on:
    - Appliance efficiency and age
    - Voltage fluctuations
    - Usage patterns
    - Environmental conditions
    
    We recommend comparing with actual bills for validation.
    """)

with st.expander("What if my bill format is different?"):
    st.markdown("""
    The system uses flexible regex patterns to handle various formats.
    If extraction fails, you can:
    - Manually enter the data
    - Use the sample bill to test features
    - Contact support for custom format handling
    """)

with st.expander("Can I track multiple properties?"):
    st.markdown("""
    Currently, the system handles one property at a time.
    You can analyze different properties by uploading different datasets.
    Multi-property tracking is planned for future versions.
    """)

st.divider()

# About Developer
st.markdown("## 👨‍💻 About")

st.markdown("""
This Smart AI Energy Advisor System was developed as a comprehensive solution to help individuals 
and organizations make data-driven decisions about their energy consumption.

**Built with:** Python, Streamlit, Pandas, Plotly, PDFPlumber, and Scikit-learn

**Purpose:** To promote energy efficiency, reduce costs, and contribute to environmental sustainability

**Version:** 1.0.0

**Last Updated:** 2024
""")

st.divider()

# Contact
st.markdown("## 📧 Feedback & Support")

st.info("""
We'd love to hear from you! Your feedback helps us improve the system.

For questions, suggestions, or support, please feel free to reach out.
""")

# Navigation
st.divider()

if st.button("← Back to Home", type="primary"):
    st.switch_page("app.py")
