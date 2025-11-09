"""
Suggestions Page - Smart AI Energy Advisor System
Provides AI-powered energy-saving recommendations and potential savings calculations.
"""

import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.analyze_data import (
    get_usage_recommendations,
    calculate_potential_savings,
    get_consumption_summary,
    identify_energy_hogs
)
from utils.visualize import create_savings_projection_chart

# Page configuration
st.set_page_config(page_title="Suggestions - Energy Advisor", page_icon="💡", layout="wide")

st.title("💡 AI-Powered Energy Saving Suggestions")
st.markdown("Personalized recommendations to reduce your energy consumption and save money")

st.divider()

# Check if data is available
if 'appliance_data' not in st.session_state or st.session_state.appliance_data is None:
    st.warning("⚠️ No appliance data found. Please upload data on the Home page first.")
    if st.button("🏠 Go to Home Page"):
        st.switch_page("pages/1_Home.py")
    st.stop()

# Get data from session state
appliance_df = st.session_state.appliance_data

# Get recommendations
recommendations = get_usage_recommendations(appliance_df)
summary = get_consumption_summary(appliance_df)

# Customized Recommendations Section
st.markdown("## 🎯 Personalized Recommendations")

if recommendations:
    st.info(f"📋 We've identified {len(recommendations)} key areas for improvement")
    
    for idx, rec in enumerate(recommendations, 1):
        with st.container():
            st.markdown(f"### {idx}. {rec['appliance']}")
            
            rec_col1, rec_col2 = st.columns([1, 2])
            
            with rec_col1:
                st.markdown("**Issue Identified:**")
                st.error(rec['issue'])
            
            with rec_col2:
                st.markdown("**Recommended Actions:**")
                st.success(rec['recommendation'])
            
            st.divider()
else:
    st.success("✅ Great! Your energy consumption pattern looks well-balanced. Keep up the good work!")

# Savings Calculator
st.markdown("## 💰 Potential Savings Calculator")

st.markdown("Estimate your potential savings by reducing energy consumption")

slider_col1, slider_col2 = st.columns([2, 1])

with slider_col1:
    reduction_target = st.slider(
        "Select target reduction percentage:",
        min_value=5,
        max_value=50,
        value=20,
        step=5,
        help="Choose how much you aim to reduce your energy consumption"
    )

with slider_col2:
    st.markdown("### Target Reduction")
    st.metric("Selected", f"{reduction_target}%")

# Calculate savings
savings = calculate_potential_savings(appliance_df, reduction_target)

# Display savings metrics
st.markdown("### 📊 Savings Projection")

savings_col1, savings_col2, savings_col3, savings_col4 = st.columns(4)

with savings_col1:
    st.metric(
        "Current Monthly Consumption",
        f"{savings['current_monthly_kwh']:.2f} kWh"
    )

with savings_col2:
    st.metric(
        "Target Monthly Consumption",
        f"{savings['target_monthly_kwh']:.2f} kWh",
        delta=f"-{savings['monthly_kwh_savings']:.2f} kWh",
        delta_color="inverse"
    )

with savings_col3:
    st.metric(
        "Monthly Cost Savings",
        f"₹{savings['monthly_cost_savings']:.2f}",
        delta=f"-{reduction_target}%",
        delta_color="inverse"
    )

with savings_col4:
    st.metric(
        "Annual Cost Savings",
        f"₹{savings['annual_cost_savings']:.2f}",
        help="Projected savings over 12 months"
    )

# Savings visualization
st.markdown("### 📈 Savings Visualization")

savings_fig = create_savings_projection_chart(
    savings['current_monthly_kwh'],
    savings['target_monthly_kwh'],
    savings['current_monthly_cost'],
    savings['target_monthly_cost']
)
st.plotly_chart(savings_fig, use_container_width=True)

st.divider()

# General Energy Saving Tips
st.markdown("## 🌟 General Energy Saving Tips")

tips_col1, tips_col2 = st.columns(2)

with tips_col1:
    st.markdown("### 🏠 Home & Appliances")
    st.markdown("""
    - **Switch to LED bulbs**: Use 75% less energy than incandescent bulbs
    - **Unplug devices**: Eliminate phantom power drain from standby mode
    - **Use power strips**: Easy way to turn off multiple devices at once
    - **Regular maintenance**: Clean filters and coils for optimal efficiency
    - **Smart thermostats**: Automatically adjust temperature based on schedule
    - **Energy-efficient appliances**: Look for 5-star rated appliances
    """)
    
    st.markdown("### ❄️ Cooling & Heating")
    st.markdown("""
    - **Optimal AC temperature**: Set to 24-26°C for comfort and efficiency
    - **Use fans**: Ceiling fans use much less energy than AC
    - **Proper insulation**: Seal doors and windows to prevent air leaks
    - **Service AC regularly**: Clean filters monthly for better performance
    - **Timer mode**: Use AC timers to avoid unnecessary cooling
    """)

with tips_col2:
    st.markdown("### 💧 Water Heating")
    st.markdown("""
    - **Lower temperature**: Set water heater to 120°F (49°C)
    - **Insulate pipes**: Reduce heat loss in hot water pipes
    - **Use timer**: Heat water only when needed
    - **Fix leaks**: Dripping hot water wastes energy
    - **Solar water heater**: Consider renewable energy option
    """)
    
    st.markdown("### 🍳 Kitchen Appliances")
    st.markdown("""
    - **Full loads only**: Run dishwasher and washing machine with full loads
    - **Air dry dishes**: Skip the heat-dry cycle on dishwashers
    - **Match pan size**: Use appropriate burner size for pots and pans
    - **Pressure cooker**: Cooks faster using less energy
    - **Microwave for small portions**: More efficient than oven for small meals
    """)

st.divider()

# Behavioral Tips
st.markdown("## 🎭 Behavioral Changes for Big Impact")

behavior_tabs = st.tabs(["⏰ Daily Habits", "📅 Weekly Actions", "🔄 Monthly Checks"])

with behavior_tabs[0]:
    st.markdown("""
    ### Daily Energy-Saving Habits
    
    1. **Turn off lights** when leaving a room
    2. **Use natural light** during daytime whenever possible
    3. **Adjust thermostat** based on occupancy
    4. **Unplug chargers** when not in use
    5. **Close refrigerator door** quickly and ensure it seals properly
    6. **Use cold water** for washing clothes when possible
    7. **Take shorter showers** to reduce water heating costs
    8. **Air dry clothes** instead of using dryer when weather permits
    """)

with behavior_tabs[1]:
    st.markdown("""
    ### Weekly Energy-Saving Actions
    
    1. **Clean AC filters** for optimal performance
    2. **Defrost freezer** if ice buildup exceeds 1/4 inch
    3. **Check for air leaks** around windows and doors
    4. **Plan laundry** to do full loads only
    5. **Review usage patterns** and adjust accordingly
    6. **Check appliance settings** for energy-saving modes
    7. **Meal prep** to reduce daily cooking time and energy use
    """)

with behavior_tabs[2]:
    st.markdown("""
    ### Monthly Energy-Saving Checks
    
    1. **Review electricity bill** for unusual spikes
    2. **Deep clean refrigerator coils** for efficiency
    3. **Inspect weather stripping** on doors and windows
    4. **Check insulation** in attic and walls
    5. **Service major appliances** according to manufacturer guidelines
    6. **Update appliance inventory** with any changes
    7. **Compare bills** month-over-month to track progress
    8. **Set energy goals** for the next month
    """)

st.divider()

# Smart Investment Recommendations
st.markdown("## 💡 Smart Investment Recommendations")

investment_col1, investment_col2 = st.columns(2)

with investment_col1:
    st.markdown("### 🔌 Quick Wins (Low Cost)")
    st.markdown("""
    - **LED Bulbs** (₹100-300 each)
        - Payback: 6-12 months
        - Savings: 75% on lighting costs
    
    - **Smart Power Strips** (₹500-1000)
        - Payback: 12-18 months
        - Eliminate phantom loads
    
    - **Door Weather Stripping** (₹200-500)
        - Payback: 3-6 months
        - Reduce AC load
    
    - **Programmable Timer** (₹300-800)
        - Payback: 6-12 months
        - Automate geyser/heater usage
    """)

with investment_col2:
    st.markdown("### 🌟 Long-term Investments (High Impact)")
    st.markdown("""
    - **5-Star Rated AC** (₹25,000-50,000)
        - Payback: 3-5 years
        - 30-40% less energy consumption
    
    - **Solar Water Heater** (₹15,000-30,000)
        - Payback: 2-4 years
        - 80% reduction in water heating cost
    
    - **Inverter Refrigerator** (₹20,000-40,000)
        - Payback: 4-6 years
        - 40-50% energy savings
    
    - **Solar Panels** (₹60,000-1,00,000/kW)
        - Payback: 5-8 years
        - Up to 90% bill reduction
    """)

st.divider()

# Action Plan
st.markdown("## 📋 Your Personalized Action Plan")

st.markdown("### 🎯 Immediate Actions (This Week)")

immediate_actions = [
    "Switch all lights to LED bulbs",
    "Set AC temperature to 25°C",
    "Unplug devices when not in use",
    "Clean AC and refrigerator filters"
]

for action in immediate_actions:
    st.checkbox(action, key=f"immediate_{action}")

st.markdown("### 📅 Short-term Goals (This Month)")

shortterm_actions = [
    "Install smart power strips",
    "Seal air leaks around doors and windows",
    "Set up water heater timer",
    "Review and optimize appliance usage schedules"
]

for action in shortterm_actions:
    st.checkbox(action, key=f"shortterm_{action}")

st.markdown("### 🚀 Long-term Plans (3-6 Months)")

longterm_actions = [
    "Replace old appliances with 5-star rated models",
    "Consider solar water heater installation",
    "Evaluate solar panel feasibility",
    "Upgrade to inverter-based appliances"
]

for action in longterm_actions:
    st.checkbox(action, key=f"longterm_{action}")

st.divider()

# Environmental Impact
st.markdown("## 🌍 Environmental Impact")

env_col1, env_col2, env_col3 = st.columns(3)

# Calculate CO2 savings (approx 0.82 kg CO2 per kWh in India)
co2_reduction = savings['monthly_kwh_savings'] * 0.82

with env_col1:
    st.metric(
        "CO₂ Reduction per Month",
        f"{co2_reduction:.2f} kg",
        help="Approximate CO₂ emissions reduced"
    )

with env_col2:
    st.metric(
        "CO₂ Reduction per Year",
        f"{co2_reduction * 12:.2f} kg",
        help="Annual CO₂ emissions reduced"
    )

with env_col3:
    trees_equivalent = (co2_reduction * 12) / 22  # One tree absorbs ~22kg CO₂/year
    st.metric(
        "Trees Equivalent",
        f"{trees_equivalent:.1f} trees",
        help="Equivalent to planting this many trees"
    )

st.success(f"🌱 By reducing {reduction_target}% of your energy consumption, you'll help fight climate change!")

# Navigation
st.divider()
nav_col1, nav_col2 = st.columns(2)

with nav_col1:
    if st.button("← Back to Analysis"):
        st.switch_page("pages/2_Analysis.py")

with nav_col2:
    if st.button("About This System →"):
        st.switch_page("pages/4_About.py")
