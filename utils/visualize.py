"""
Utility module for creating interactive visualizations using Plotly.
Generates charts and graphs for energy consumption analysis.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Any


def create_consumption_pie_chart(appliance_df: pd.DataFrame) -> go.Figure:
    """
    Create a pie chart showing energy consumption distribution by appliance.
    
    Args:
        appliance_df: DataFrame with appliance consumption data
        
    Returns:
        Plotly figure object
    """
    from utils.analyze_data import calculate_appliance_consumption
    
    df = calculate_appliance_consumption(appliance_df)
    
    fig = px.pie(
        df,
        values='monthly_kwh',
        names='appliance',
        title='Energy Consumption Distribution by Appliance',
        hole=0.3,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Consumption: %{value:.2f} kWh<br>Percentage: %{percent}<extra></extra>'
    )
    
    return fig


def create_consumption_bar_chart(appliance_df: pd.DataFrame) -> go.Figure:
    """
    Create a bar chart showing monthly consumption by appliance.
    
    Args:
        appliance_df: DataFrame with appliance consumption data
        
    Returns:
        Plotly figure object
    """
    from utils.analyze_data import calculate_appliance_consumption
    
    df = calculate_appliance_consumption(appliance_df)
    df = df.sort_values('monthly_kwh', ascending=False)
    
    fig = px.bar(
        df,
        x='appliance',
        y='monthly_kwh',
        title='Monthly Energy Consumption by Appliance',
        labels={'monthly_kwh': 'Monthly Consumption (kWh)', 'appliance': 'Appliance'},
        color='monthly_kwh',
        color_continuous_scale='Blues'
    )
    
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Consumption: %{y:.2f} kWh<extra></extra>'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False
    )
    
    return fig


def create_cost_comparison_chart(appliance_df: pd.DataFrame) -> go.Figure:
    """
    Create a comparison chart showing consumption vs cost.
    
    Args:
        appliance_df: DataFrame with appliance consumption data
        
    Returns:
        Plotly figure object
    """
    from utils.analyze_data import calculate_appliance_consumption
    
    df = calculate_appliance_consumption(appliance_df)
    df = df.sort_values('monthly_cost', ascending=False)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['appliance'],
        y=df['monthly_kwh'],
        name='Monthly kWh',
        marker_color='lightblue',
        yaxis='y',
        hovertemplate='<b>%{x}</b><br>Consumption: %{y:.2f} kWh<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        x=df['appliance'],
        y=df['monthly_cost'],
        name='Monthly Cost (₹)',
        marker_color='lightcoral',
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>Cost: ₹%{y:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Energy Consumption vs Cost Comparison',
        xaxis=dict(title='Appliance', tickangle=-45),
        yaxis=dict(title=dict(text='Monthly Consumption (kWh)', font=dict(color='lightblue'))),
        yaxis2=dict(title=dict(text='Monthly Cost (₹)', font=dict(color='lightcoral')), overlaying='y', side='right'),
        barmode='group',
        hovermode='x unified'
    )
    
    return fig


def create_category_distribution(appliance_df: pd.DataFrame) -> go.Figure:
    """
    Create a chart showing distribution of appliances by consumption category.
    
    Args:
        appliance_df: DataFrame with appliance consumption data
        
    Returns:
        Plotly figure object
    """
    from utils.analyze_data import categorize_appliances
    
    df = categorize_appliances(appliance_df)
    category_counts = df['consumption_category'].value_counts()
    
    fig = px.bar(
        x=category_counts.index,
        y=category_counts.values,
        title='Appliance Distribution by Consumption Category',
        labels={'x': 'Consumption Category', 'y': 'Number of Appliances'},
        color=category_counts.index,
        color_discrete_map={
            'Low': 'green',
            'Medium': 'yellow',
            'High': 'orange',
            'Very High': 'red'
        }
    )
    
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Count: %{y} appliances<extra></extra>'
    )
    
    return fig


def create_daily_vs_monthly_chart(appliance_df: pd.DataFrame) -> go.Figure:
    """
    Create a grouped bar chart comparing daily and monthly consumption.
    
    Args:
        appliance_df: DataFrame with appliance consumption data
        
    Returns:
        Plotly figure object
    """
    from utils.analyze_data import calculate_appliance_consumption
    
    df = calculate_appliance_consumption(appliance_df)
    df = df.sort_values('monthly_kwh', ascending=False).head(10)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['appliance'],
        y=df['daily_kwh'],
        name='Daily Consumption (kWh)',
        marker_color='steelblue'
    ))
    
    fig.add_trace(go.Bar(
        x=df['appliance'],
        y=df['monthly_kwh'],
        name='Monthly Consumption (kWh)',
        marker_color='darkblue'
    ))
    
    fig.update_layout(
        title='Daily vs Monthly Energy Consumption (Top 10 Appliances)',
        xaxis_title='Appliance',
        yaxis_title='Energy Consumption (kWh)',
        barmode='group',
        xaxis_tickangle=-45,
        hovermode='x unified'
    )
    
    return fig


def create_savings_projection_chart(current_kwh: float, target_kwh: float, 
                                   current_cost: float, target_cost: float) -> go.Figure:
    """
    Create a chart showing potential savings.
    
    Args:
        current_kwh: Current monthly kWh consumption
        target_kwh: Target monthly kWh after reduction
        current_cost: Current monthly cost
        target_cost: Target monthly cost after reduction
        
    Returns:
        Plotly figure object
    """
    categories = ['Current', 'Target', 'Savings']
    kwh_values = [current_kwh, target_kwh, current_kwh - target_kwh]
    cost_values = [current_cost, target_cost, current_cost - target_cost]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=categories,
        y=kwh_values,
        name='Energy (kWh)',
        marker_color=['red', 'green', 'blue'],
        text=[f'{v:.2f} kWh' for v in kwh_values],
        textposition='auto',
    ))
    
    fig.update_layout(
        title='Potential Energy Savings Projection',
        yaxis_title='Monthly Energy Consumption (kWh)',
        showlegend=False,
        hovermode='x unified'
    )
    
    return fig


def create_gauge_chart(value: float, max_value: float, title: str = "Efficiency Score") -> go.Figure:
    """
    Create a gauge chart for displaying scores.
    
    Args:
        value: Current value
        max_value: Maximum value
        title: Chart title
        
    Returns:
        Plotly figure object
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        delta={'reference': max_value * 0.7},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, max_value * 0.33], 'color': "lightcoral"},
                {'range': [max_value * 0.33, max_value * 0.66], 'color': "lightyellow"},
                {'range': [max_value * 0.66, max_value], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.8
            }
        }
    ))
    
    fig.update_layout(height=300)
    
    return fig
