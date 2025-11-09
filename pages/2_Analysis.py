"""
Analysis Page - Smart AI Energy Advisor System
Displays detailed energy consumption analysis with interactive charts and insights.
"""

import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.analyze_data import (
    calculate_appliance_consumption,
    get_consumption_summary,
    categorize_appliances,
    identify_energy_hogs,
    calculate_efficiency_score
)
from utils.visualize import (
    create_consumption_pie_chart,
    create_consumption_bar_chart,
    create_cost_comparison_chart,
    create_category_distribution,
    create_daily_vs_monthly_chart,
    create_gauge_chart
)

# Page configuration
st.set_page_config(page_title="Analysis - Energy Advisor", page_icon="📊", layout="wide")

st.title("📊 Energy Consumption Analysis")
st.markdown("Comprehensive analysis of your energy usage patterns")

st.divider()

# Check if data is available
if 'appliance_data' not in st.session_state or st.session_state.appliance_data is None:
    st.warning("⚠️ No appliance data found. Please upload data on the Home page first.")
    if st.button("🏠 Go to Home Page"):
        st.switch_page("pages/1_Home.py")
    st.stop()

# Get data from session state
appliance_df = st.session_state.appliance_data
bill_data = st.session_state.get('bill_data', None)

# Calculate consumption
consumption_df = calculate_appliance_consumption(appliance_df)
summary = get_consumption_summary(appliance_df)

# Overview Section
st.markdown("## 📈 Consumption Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Monthly Consumption",
        f"{summary['total_monthly_kwh']:.2f} kWh",
        help="Total energy consumed per month by all appliances"
    )

with col2:
    st.metric(
        "Total Monthly Cost",
        f"₹{summary['total_monthly_cost']:.2f}",
        help="Estimated monthly electricity cost"
    )

with col3:
    st.metric(
        "Average Daily Consumption",
        f"{summary['total_daily_kwh']:.2f} kWh",
        help="Average energy consumed per day"
    )

with col4:
    st.metric(
        "Number of Appliances",
        summary['appliance_count'],
        help="Total number of appliances tracked"
    )

st.divider()

# Efficiency Score
st.markdown("## 🎯 Efficiency Analysis")

bill_units = bill_data['metered_units'] if bill_data else None
efficiency = calculate_efficiency_score(appliance_df, bill_units)

eff_col1, eff_col2 = st.columns([1, 2])

with eff_col1:
    # Gauge chart for efficiency score
    gauge_fig = create_gauge_chart(efficiency['efficiency_score'], 100, "Efficiency Score")
    st.plotly_chart(gauge_fig, use_container_width=True)

with eff_col2:
    st.markdown("### Efficiency Metrics")
    
    metrics_col1, metrics_col2 = st.columns(2)
    
    with metrics_col1:
        st.metric("Efficiency Score", f"{efficiency['efficiency_score']:.2f}/100")
        st.metric("Consumption Balance", efficiency['consumption_balance'])
    
    with metrics_col2:
        st.metric("Calculated Monthly Consumption", f"{efficiency['calculated_monthly_kwh']:.2f} kWh")
        
        if bill_units:
            st.metric("Actual Bill Units", f"{efficiency['bill_units']:.2f} kWh")
            st.metric("Difference", f"{efficiency['difference']:.2f} kWh ({efficiency['difference_percentage']:.1f}%)")
            
            if efficiency['accuracy'] == 'Good':
                st.success(f"✅ Accuracy: {efficiency['accuracy']}")
            elif efficiency['accuracy'] == 'Fair':
                st.info(f"ℹ️ Accuracy: {efficiency['accuracy']}")
            else:
                st.warning(f"⚠️ Accuracy: {efficiency['accuracy']}")

st.divider()

# Detailed Analysis
st.markdown("## 📊 Detailed Consumption Analysis")

# Tabs for different views
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Distribution", 
    "📈 Comparison", 
    "🏷️ Categories",
    "📅 Daily vs Monthly"
])

with tab1:
    st.markdown("### Energy Consumption Distribution")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Pie chart
        pie_fig = create_consumption_pie_chart(appliance_df)
        st.plotly_chart(pie_fig, use_container_width=True)
    
    with chart_col2:
        # Bar chart
        bar_fig = create_consumption_bar_chart(appliance_df)
        st.plotly_chart(bar_fig, use_container_width=True)

with tab2:
    st.markdown("### Consumption vs Cost Comparison")
    cost_fig = create_cost_comparison_chart(appliance_df)
    st.plotly_chart(cost_fig, use_container_width=True)

with tab3:
    st.markdown("### Appliance Categories by Consumption Level")
    
    cat_col1, cat_col2 = st.columns([1, 2])
    
    with cat_col1:
        categorized_df = categorize_appliances(appliance_df)
        category_counts = categorized_df['consumption_category'].value_counts()
        
        st.markdown("#### Category Distribution")
        for category, count in category_counts.items():
            color = {'Low': '🟢', 'Medium': '🟡', 'High': '🟠', 'Very High': '🔴'}
            st.markdown(f"{color.get(category, '⚪')} **{category}**: {count} appliances")
    
    with cat_col2:
        cat_fig = create_category_distribution(appliance_df)
        st.plotly_chart(cat_fig, use_container_width=True)

with tab4:
    st.markdown("### Daily vs Monthly Consumption Comparison")
    daily_monthly_fig = create_daily_vs_monthly_chart(appliance_df)
    st.plotly_chart(daily_monthly_fig, use_container_width=True)

st.divider()

# Top Energy Consumers
st.markdown("## 🔝 Top Energy Consumers")

energy_hogs = identify_energy_hogs(appliance_df, threshold_percentage=10)

if energy_hogs:
    st.warning(f"⚠️ {len(energy_hogs)} appliance(s) consuming more than 10% of total energy")
    
    hog_df = pd.DataFrame(energy_hogs)
    
    for idx, hog in enumerate(energy_hogs):
        with st.expander(f"🔴 {hog['appliance']} - {hog['percentage']:.1f}% of total consumption"):
            hog_col1, hog_col2, hog_col3 = st.columns(3)
            
            with hog_col1:
                st.metric("Monthly Consumption", f"{hog['monthly_kwh']:.2f} kWh")
            with hog_col2:
                st.metric("Percentage of Total", f"{hog['percentage']:.1f}%")
            with hog_col3:
                st.metric("Monthly Cost", f"₹{hog['monthly_cost']:.2f}")
else:
    st.success("✅ Good news! No single appliance is consuming excessive energy.")

st.divider()

# Detailed Appliance Table
st.markdown("## 📋 Detailed Appliance Breakdown")

# Display the detailed consumption table
display_df = consumption_df[['appliance', 'wattage', 'hours_per_day', 'quantity', 
                              'daily_kwh', 'monthly_kwh', 'monthly_cost']].copy()

display_df.columns = ['Appliance', 'Wattage (W)', 'Hours/Day', 'Quantity', 
                       'Daily (kWh)', 'Monthly (kWh)', 'Monthly Cost (₹)']

# Format numeric columns
display_df['Daily (kWh)'] = display_df['Daily (kWh)'].round(2)
display_df['Monthly (kWh)'] = display_df['Monthly (kWh)'].round(2)
display_df['Monthly Cost (₹)'] = display_df['Monthly Cost (₹)'].round(2)

# Sort by monthly consumption
display_df = display_df.sort_values('Monthly (kWh)', ascending=False)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# Download option
csv_data = display_df.to_csv(index=False)
st.download_button(
    label="📥 Download Detailed Report (CSV)",
    data=csv_data,
    file_name="energy_consumption_analysis.csv",
    mime="text/csv"
)

st.divider()

# Summary insights
st.markdown("## 💡 Key Insights")

insights_col1, insights_col2 = st.columns(2)

with insights_col1:
    st.markdown("### 📌 Consumption Patterns")
    
    top_3 = summary['top_consumers'][:3]
    st.markdown("**Top 3 Energy Consumers:**")
    for i, consumer in enumerate(top_3, 1):
        st.markdown(f"{i}. **{consumer['appliance']}**: {consumer['monthly_kwh']:.2f} kWh/month")
    
    avg_per_appliance = summary['total_monthly_kwh'] / summary['appliance_count']
    st.info(f"Average consumption per appliance: {avg_per_appliance:.2f} kWh/month")

with insights_col2:
    st.markdown("### 💰 Cost Breakdown")
    
    st.metric("Daily Cost", f"₹{summary['total_monthly_cost']/30:.2f}")
    st.metric("Weekly Cost", f"₹{summary['total_monthly_cost']/4.33:.2f}")
    st.metric("Annual Projection", f"₹{summary['total_monthly_cost']*12:.2f}")

# Navigation
st.divider()
nav_col1, nav_col2 = st.columns(2)

with nav_col1:
    if st.button("← Back to Home"):
        st.switch_page("pages/1_Home.py")

with nav_col2:
    if st.button("Get Suggestions →", type="primary"):
        st.switch_page("pages/3_Suggestions.py")
