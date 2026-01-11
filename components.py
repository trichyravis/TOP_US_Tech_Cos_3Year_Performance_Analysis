"""
Components Module - Reusable UI building blocks
Purpose: DRY principle for common widgets and layouts
"""

import streamlit as st
import pandas as pd
from config import TICKERS, COLORS
import plotly.graph_objects as go

def render_company_selector(mode='single', default=None):
    """
    Render company selection widget
    Args:
        mode (str): 'single' or 'multi'
        default (str or list): Default selection
    Returns:
        str or list: Selected ticker(s)
    """
    if mode == 'single':
        selected = st.selectbox(
            "Select Company:",
            options=list(TICKERS.keys()),
            format_func=lambda x: f"{x} - {TICKERS[x]}",
            key=f"company_selector_{id(default)}",
            index=0 if not default else (list(TICKERS.keys()).index(default) if default in TICKERS else 0)
        )
        return selected
    else:
        selected = st.multiselect(
            "Select Companies:",
            options=list(TICKERS.keys()),
            format_func=lambda x: f"{x} - {TICKERS[x]}",
            default=default or ['NVDA', 'MSFT']
        )
        if not selected:
            st.error("Select at least one company")
            st.stop()
        return selected


def render_date_range_picker(label="Select Date Range", max_days=1095):
    """
    Render date range picker with validation
    Args:
        label (str): Widget label
        max_days (int): Maximum range in days
    Returns:
        tuple: (start_date, end_date)
    """
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "Start Date:",
            value=pd.Timestamp.now() - pd.Timedelta(days=max_days)
        )
    
    with col2:
        end_date = st.date_input(
            "End Date:",
            value=pd.Timestamp.now()
        )
    
    if start_date >= end_date:
        st.error("Start date must be before end date")
        st.stop()
    
    return start_date, end_date


def render_confidence_level_selector(default=0.95):
    """
    Render VaR confidence level selector
    Args:
        default (float): Default confidence level (0.90, 0.95, 0.99)
    Returns:
        float: Selected confidence level
    """
    options = {
        '90% Confidence': 0.90,
        '95% Confidence (Default)': 0.95,
        '99% Confidence': 0.99
    }
    
    selected = st.radio(
        "Confidence Level for VaR:",
        options=list(options.keys()),
        index=1  # 95% as default
    )
    
    return options[selected]


def render_metrics_row(metrics_dict, columns=3):
    """
    Render multiple metrics in a row
    Args:
        metrics_dict (dict): {label: value, ...}
        columns (int): Number of columns
    Returns:
        None (displays metrics)
    """
    cols = st.columns(columns)
    
    for idx, (label, value) in enumerate(metrics_dict.items()):
        with cols[idx % columns]:
            st.metric(
                label=label,
                value=f"{value:.2f}" if isinstance(value, (int, float)) else value
            )


def render_data_table(df, column_config=None, hide_index=True):
    """
    Render styled data table
    Args:
        df (pd.DataFrame): Data to display
        column_config (dict): Column formatting
        hide_index (bool): Hide row index
    Returns:
        None (displays table)
    """
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=hide_index,
        column_config=column_config or {}
    )


def render_candlestick_chart(ohlc_data, title="Price Movement"):
    """
    Render interactive candlestick chart
    Args:
        ohlc_data (pd.DataFrame): OHLC data with columns [Open, High, Low, Close]
        title (str): Chart title
    Returns:
        None (displays chart)
    """
    fig = go.Figure(data=[go.Candlestick(
        x=ohlc_data.index,
        open=ohlc_data['Open'],
        high=ohlc_data['High'],
        low=ohlc_data['Low'],
        close=ohlc_data['Close']
    )])
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price ($)",
        template="plotly_white",
        hovermode="x unified",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_comparison_chart(data_dict, metric_name="Annual Returns", chart_type='bar'):
    """
    Render comparison chart across multiple companies
    Args:
        data_dict (dict): {ticker: value, ...}
        metric_name (str): Metric being compared
        chart_type (str): 'bar' or 'line'
    Returns:
        None (displays chart)
    """
    fig = go.Figure()
    
    if chart_type == 'bar':
        fig.add_trace(go.Bar(
            x=list(data_dict.keys()),
            y=list(data_dict.values()),
            marker_color=[COLORS.get(ticker, COLORS['primary']) 
                         for ticker in data_dict.keys()]
        ))
    else:
        fig.add_trace(go.Scatter(
            x=list(data_dict.keys()),
            y=list(data_dict.values()),
            mode='lines+markers'
        ))
    
    fig.update_layout(
        title=f"{metric_name} Comparison",
        xaxis_title="Company",
        yaxis_title=metric_name,
        template="plotly_white",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_sidebar_header(title, icon="📊"):
    """
    Render styled sidebar header
    Args:
        title (str): Header text
        icon (str): Emoji icon
    Returns:
        None (displays header)
    """
    st.sidebar.markdown(f"## {icon} {title}")
    st.sidebar.divider()


def render_disclaimer_box():
    """
    Render prominent disclaimer box
    Returns: None (displays disclaimer)
    """
    from config import DISCLAIMER
    st.warning(DISCLAIMER)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def format_currency(value):
    """Format number as currency (USD)"""
    if value >= 1e9:
        return f"${value/1e9:.2f}B"
    elif value >= 1e6:
        return f"${value/1e6:.2f}M"
    else:
        return f"${value:,.0f}"


def format_percentage(value, decimals=2):
    """Format number as percentage"""
    return f"{value*100:.{decimals}f}%"


def format_ratio(value, decimals=2):
    """Format ratio (e.g., Sharpe ratio)"""
    return f"{value:.{decimals}f}x"
