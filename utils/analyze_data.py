"""
Utility module for analyzing energy consumption data.
Provides functions for statistical analysis, pattern detection, and consumption insights.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any


def calculate_appliance_consumption(appliance_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate energy consumption for each appliance based on wattage and usage hours.
    
    Args:
        appliance_df: DataFrame with columns: appliance, wattage, hours_per_day, quantity
        
    Returns:
        DataFrame with additional columns for daily and monthly consumption
    """
    df = appliance_df.copy()
    
    # Calculate daily consumption in kWh
    df['daily_kwh'] = (df['wattage'] * df['hours_per_day'] * df['quantity']) / 1000
    
    # Calculate monthly consumption (30 days)
    df['monthly_kwh'] = df['daily_kwh'] * 30
    
    # Calculate cost (assuming average rate per kWh)
    avg_rate = 6.5  # Default rate in rupees per kWh
    df['monthly_cost'] = df['monthly_kwh'] * avg_rate
    
    return df


def get_consumption_summary(appliance_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate summary statistics for energy consumption.
    
    Args:
        appliance_df: DataFrame with appliance consumption data
        
    Returns:
        Dictionary with summary statistics
    """
    df = calculate_appliance_consumption(appliance_df)
    
    summary = {
        'total_daily_kwh': df['daily_kwh'].sum(),
        'total_monthly_kwh': df['monthly_kwh'].sum(),
        'total_monthly_cost': df['monthly_cost'].sum(),
        'avg_daily_kwh': df['daily_kwh'].mean(),
        'top_consumers': df.nlargest(5, 'monthly_kwh')[['appliance', 'monthly_kwh', 'monthly_cost']].to_dict('records'),
        'appliance_count': len(df),
        'total_wattage': (df['wattage'] * df['quantity']).sum()
    }
    
    return summary


def categorize_appliances(appliance_df: pd.DataFrame) -> pd.DataFrame:
    """
    Categorize appliances by consumption level.
    
    Args:
        appliance_df: DataFrame with appliance data
        
    Returns:
        DataFrame with category column added
    """
    df = calculate_appliance_consumption(appliance_df)
    
    # Define consumption categories based on monthly kWh
    def categorize(kwh):
        if kwh < 10:
            return 'Low'
        elif kwh < 50:
            return 'Medium'
        elif kwh < 150:
            return 'High'
        else:
            return 'Very High'
    
    df['consumption_category'] = df['monthly_kwh'].apply(categorize)
    
    return df


def identify_energy_hogs(appliance_df: pd.DataFrame, threshold_percentage: float = 20) -> List[Dict]:
    """
    Identify appliances that consume disproportionate energy.
    
    Args:
        appliance_df: DataFrame with appliance data
        threshold_percentage: Percentage threshold to identify energy hogs
        
    Returns:
        List of appliances consuming above threshold percentage
    """
    df = calculate_appliance_consumption(appliance_df)
    total_consumption = df['monthly_kwh'].sum()
    
    energy_hogs = []
    for _, row in df.iterrows():
        percentage = (row['monthly_kwh'] / total_consumption) * 100
        if percentage >= threshold_percentage:
            energy_hogs.append({
                'appliance': row['appliance'],
                'monthly_kwh': row['monthly_kwh'],
                'percentage': percentage,
                'monthly_cost': row['monthly_cost']
            })
    
    return sorted(energy_hogs, key=lambda x: x['percentage'], reverse=True)


def calculate_efficiency_score(appliance_df: pd.DataFrame, total_bill_units: float = None) -> Dict[str, Any]:
    """
    Calculate overall energy efficiency score based on consumption patterns.
    
    Args:
        appliance_df: DataFrame with appliance data
        total_bill_units: Total units from actual bill (optional)
        
    Returns:
        Dictionary with efficiency metrics
    """
    df = calculate_appliance_consumption(appliance_df)
    total_calculated = df['monthly_kwh'].sum()
    
    # Calculate variance in consumption
    consumption_std = df['monthly_kwh'].std()
    consumption_mean = df['monthly_kwh'].mean()
    
    # Efficiency score (0-100, higher is better balanced consumption)
    if consumption_mean > 0:
        coefficient_of_variation = (consumption_std / consumption_mean) * 100
        efficiency_score = max(0, 100 - coefficient_of_variation)
    else:
        efficiency_score = 0
    
    result = {
        'efficiency_score': round(efficiency_score, 2),
        'calculated_monthly_kwh': total_calculated,
        'consumption_balance': 'Balanced' if coefficient_of_variation < 50 else 'Unbalanced'
    }
    
    # Compare with actual bill if provided
    if total_bill_units:
        difference = abs(total_calculated - total_bill_units)
        difference_percentage = (difference / total_bill_units) * 100
        result['bill_units'] = total_bill_units
        result['difference'] = difference
        result['difference_percentage'] = round(difference_percentage, 2)
        result['accuracy'] = 'Good' if difference_percentage < 15 else 'Fair' if difference_percentage < 30 else 'Poor'
    
    return result


def get_usage_recommendations(appliance_df: pd.DataFrame) -> List[Dict[str, str]]:
    """
    Generate usage recommendations based on consumption patterns.
    
    Args:
        appliance_df: DataFrame with appliance data
        
    Returns:
        List of recommendation dictionaries
    """
    df = calculate_appliance_consumption(appliance_df)
    recommendations = []
    
    # Identify high-consumption appliances
    energy_hogs = identify_energy_hogs(df, threshold_percentage=15)
    
    for hog in energy_hogs:
        appliance_name = hog['appliance']
        percentage = hog['percentage']
        
        if 'AC' in appliance_name.upper() or 'AIR CONDITIONER' in appliance_name.upper():
            recommendations.append({
                'appliance': appliance_name,
                'issue': f"Consuming {percentage:.1f}% of total energy",
                'recommendation': "Set temperature to 24-26°C, use timer mode, clean filters monthly"
            })
        elif 'REFRIGERATOR' in appliance_name.upper() or 'FRIDGE' in appliance_name.upper():
            recommendations.append({
                'appliance': appliance_name,
                'issue': f"Consuming {percentage:.1f}% of total energy",
                'recommendation': "Ensure door seals are tight, set optimal temperature (3-4°C), defrost regularly"
            })
        elif 'HEATER' in appliance_name.upper() or 'GEYSER' in appliance_name.upper():
            recommendations.append({
                'appliance': appliance_name,
                'issue': f"Consuming {percentage:.1f}% of total energy",
                'recommendation': "Use timer, reduce temperature setting, insulate pipes, consider solar heating"
            })
        else:
            recommendations.append({
                'appliance': appliance_name,
                'issue': f"Consuming {percentage:.1f}% of total energy",
                'recommendation': "Reduce usage hours, use energy-efficient alternatives, unplug when not in use"
            })
    
    return recommendations


def calculate_potential_savings(appliance_df: pd.DataFrame, reduction_percentage: float = 20) -> Dict[str, Any]:
    """
    Calculate potential savings from reducing consumption.
    
    Args:
        appliance_df: DataFrame with appliance data
        reduction_percentage: Target reduction percentage
        
    Returns:
        Dictionary with savings projections
    """
    df = calculate_appliance_consumption(appliance_df)
    
    current_monthly_kwh = df['monthly_kwh'].sum()
    current_monthly_cost = df['monthly_cost'].sum()
    
    reduced_kwh = current_monthly_kwh * (1 - reduction_percentage / 100)
    reduced_cost = current_monthly_cost * (1 - reduction_percentage / 100)
    
    savings = {
        'current_monthly_kwh': round(current_monthly_kwh, 2),
        'current_monthly_cost': round(current_monthly_cost, 2),
        'target_monthly_kwh': round(reduced_kwh, 2),
        'target_monthly_cost': round(reduced_cost, 2),
        'monthly_kwh_savings': round(current_monthly_kwh - reduced_kwh, 2),
        'monthly_cost_savings': round(current_monthly_cost - reduced_cost, 2),
        'annual_cost_savings': round((current_monthly_cost - reduced_cost) * 12, 2),
        'reduction_percentage': reduction_percentage
    }
    
    return savings
