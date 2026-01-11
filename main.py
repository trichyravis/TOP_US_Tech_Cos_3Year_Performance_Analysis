
"""
Main Application File - Streamlit Entry Point
Uses proven DataFetcher pattern for robust data loading
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

from data_handler import (
    DataFetcher, fetch_all_company_data, fetch_market_data, get_company_data
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="TOP US Tech Companies Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Mountain Path Theme
st.markdown("""
<style>
    [data-testid="stHeader"] {
        background-color: #003366 !important;
    }
    
    .main {
        background-color: #f8f9fa;
    }
    
    [data-testid="stSidebar"] {
        background-color: #003366;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #003366 0%, #004d80 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    h1, h2, h3 {
        color: #003366;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        color: #003366;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #003366 0%, #004d80 100%); 
                padding: 30px; border-radius: 15px; text-align: center; margin: 20px 0;">
        <h1 style="color: #FFD700; margin: 0;">THE MOUNTAIN PATH - WORLD OF FINANCE</h1>
        <p style="color: white; font-size: 18px; margin: 10px 0;">Top US Tech Companies Performance Analysis</p>
        <p style="color: #FFD700; font-size: 14px; margin: 0;">3-Year Rolling Window • Educational Purpose Only</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### 🔧 Controls")
    
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### ⚙️ Risk Parameters")
    confidence_level = st.radio(
        "VaR Confidence Level:",
        [90, 95, 99],
        index=1
    )

# ============================================================================
# MAIN TABS
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 About Platform",
    "💰 Financial Performance",
    "📈 Market Analysis",
    "⚠️ Risk Analysis",
    "📊 Summary & Insights"
])

# ============================================================================
# TAB 1: ABOUT
# ============================================================================

with tab1:
    st.subheader("📚 About The Mountain Path - World of Finance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Platform Overview
        
        **The Mountain Path - World of Finance** is an educational platform 
        designed to help students understand:
        
        - Financial analysis and valuation
        - Investment concepts and strategies
        - Risk management frameworks
        - Quantitative finance techniques
        
        ### This Tool
        
        This dashboard analyzes the **Top 5 US Technology Companies**:
        - **NVDA** - NVIDIA (Semiconductors)
        - **MSFT** - Microsoft (Cloud & Software)
        - **AAPL** - Apple (Consumer Electronics)
        - **GOOGL** - Alphabet (Search & Advertising)
        - **AMZN** - Amazon (E-commerce & Cloud)
        """)
    
    with col2:
        st.markdown("""
        ### Data Sources
        
        - **Price Data**: Yahoo Finance (yfinance)
        - **Financial Metrics**: Company financial statements
        - **Index Data**: S&P 500 (^GSPC)
        - **Time Period**: 3-Year rolling window
        
        ### Metrics Calculated
        
        - **Returns & Volatility**: Daily returns, annualized metrics
        - **Risk Ratios**: Sharpe ratio, Sortino ratio
        - **Drawdown Analysis**: Maximum drawdown, recovery periods
        - **Value Metrics**: P/E, P/B, Price-to-Sales ratios
        - **Leverage Ratios**: Debt-to-Equity, Current Ratio
        
        ---
        
        **Prof. V. Ravichandran**
        
        28+ Years Corporate Finance & Banking Experience
        
        10+ Years Academic Excellence
        """)

# ============================================================================
# TAB 2: FINANCIAL PERFORMANCE
# ============================================================================

with tab2:
    st.subheader("💰 Financial Performance - All TOP US Tech Companies")
    
    st.info("📊 Loading financial data for all 5 companies...")
    
    try:
        # Fetch all company data
        all_data = fetch_all_company_data()
        
        if not all_data:
            st.error("❌ Could not fetch financial data. Please try refreshing.")
        else:
            # Build financial metrics table
            financial_rows = []
            
            for ticker, data in all_data.items():
                company_info = data.get('company_info', {})
                info = data.get('info', {})
                
                financial_rows.append({
                    'Company': f"{ticker} - {company_info.get('name', 'Unknown')}",
                    'Sector': company_info.get('sector', 'N/A'),
                    'Revenue ($B)': (info.get('totalRevenue', 0) or 0) / 1e9,
                    'Operating Income ($B)': (info.get('operatingIncome', 0) or 0) / 1e9,
                    'Net Income ($B)': (info.get('netIncome', 0) or 0) / 1e9,
                    'Market Cap ($B)': (info.get('marketCap', 0) or 0) / 1e9,
                })
            
            df_financial = pd.DataFrame(financial_rows)
            
            # Summary metrics
            st.subheader("📊 Summary Metrics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                max_revenue = df_financial['Revenue ($B)'].max()
                st.metric("Highest Revenue", f"${max_revenue:.1f}B")
            with col2:
                max_income = df_financial['Net Income ($B)'].max()
                st.metric("Highest Net Income", f"${max_income:.1f}B")
            with col3:
                max_cap = df_financial['Market Cap ($B)'].max()
                st.metric("Largest Market Cap", f"${max_cap:.1f}B")
            
            # Financial comparison table
            st.subheader("Financial Metrics Comparison")
            st.dataframe(
                df_financial.style.format({
                    'Revenue ($B)': '{:.1f}',
                    'Operating Income ($B)': '{:.1f}',
                    'Net Income ($B)': '{:.1f}',
                    'Market Cap ($B)': '{:.1f}'
                }),
                use_container_width=True
            )
            
            # Individual company details
            st.subheader("📈 Individual Company Details")
            
            for ticker, data in all_data.items():
                company_info = data.get('company_info', {})
                info = data.get('info', {})
                
                with st.expander(f"📊 {ticker} - {company_info.get('name', 'Unknown')}"):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        revenue = (info.get('totalRevenue', 0) or 0) / 1e9
                        st.metric("Revenue", f"${revenue:.1f}B")
                    with col2:
                        op_income = (info.get('operatingIncome', 0) or 0) / 1e9
                        st.metric("Operating Income", f"${op_income:.1f}B")
                    with col3:
                        net_income = (info.get('netIncome', 0) or 0) / 1e9
                        st.metric("Net Income", f"${net_income:.1f}B")
                    with col4:
                        market_cap = (info.get('marketCap', 0) or 0) / 1e9
                        st.metric("Market Cap", f"${market_cap:.1f}B")
                    
                    # Additional metrics
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        pe = info.get('trailingPE')
                        if pe:
                            st.metric("P/E Ratio", f"{pe:.2f}")
                        else:
                            st.metric("P/E Ratio", "N/A")
                    
                    with col2:
                        pb = info.get('priceToBook')
                        if pb:
                            st.metric("P/B Ratio", f"{pb:.2f}")
                        else:
                            st.metric("P/B Ratio", "N/A")
                    
                    with col3:
                        yield_val = info.get('dividendYield')
                        if yield_val:
                            st.metric("Dividend Yield", f"{yield_val*100:.2f}%")
                        else:
                            st.metric("Dividend Yield", "N/A")
    
    except Exception as e:
        st.error(f"❌ Error loading financial data: {str(e)}")
        st.info("💡 Please try clicking 'Refresh Data' button in the sidebar")

# ============================================================================
# TAB 3: MARKET ANALYSIS
# ============================================================================

with tab3:
    st.subheader("📈 Market Analysis - All TOP US Tech Companies")
    
    st.info("📊 Analyzing all 5 companies: NVDA, MSFT, AAPL, GOOGL, AMZN")
    
    try:
        all_data = fetch_all_company_data()
        
        if not all_data:
            st.error("❌ Could not fetch price data")
        else:
            # Candlestick charts for each company
            st.subheader("📉 Candlestick Charts")
            
            chart_tabs = st.tabs([
                "NVDA - NVIDIA",
                "MSFT - Microsoft",
                "AAPL - Apple",
                "GOOGL - Alphabet",
                "AMZN - Amazon"
            ])
            
            for idx, (ticker, data) in enumerate(all_data.items()):
                with chart_tabs[idx]:
                    price_data = data.get('price_data')
                    company_info = data.get('company_info', {})
                    
                    if price_data is not None and not price_data.empty:
                        # Ensure column names are correct
                        cols = price_data.columns.str.lower()
                        price_data.columns = cols
                        
                        fig = go.Figure(data=[go.Candlestick(
                            x=price_data.index,
                            open=price_data['open'],
                            high=price_data['high'],
                            low=price_data['low'],
                            close=price_data['close']
                        )])
                        
                        fig.update_layout(
                            title=f"{ticker} - {company_info.get('name', 'Unknown')} (3-Year Candlestick)",
                            xaxis_title="Date",
                            yaxis_title="Price ($)",
                            template="plotly_white",
                            height=500,
                            hovermode="x unified"
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning(f"Could not load price data for {ticker}")
            
            # Annual returns comparison
            st.subheader("📊 Annual Returns Comparison")
            
            annual_returns = {}
            for ticker, data in all_data.items():
                price_data = data.get('price_data')
                if price_data is not None and not price_data.empty:
                    cols = price_data.columns.str.lower()
                    price_data.columns = cols
                    annual_return = DataFetcher.calculate_annual_return(price_data['close'])
                    annual_returns[ticker] = annual_return * 100
            
            if annual_returns:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=list(annual_returns.keys()),
                    y=list(annual_returns.values()),
                    marker_color=['#FFD700' if v > 0 else '#ff6b6b' for v in annual_returns.values()],
                    text=[f"{v:.1f}%" for v in annual_returns.values()],
                    textposition="auto",
                ))
                
                fig.update_layout(
                    title="3-Year Annualized Returns",
                    xaxis_title="Company",
                    yaxis_title="Annual Return (%)",
                    template="plotly_white",
                    height=400,
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Volatility comparison
            st.subheader("📈 Volatility Comparison")
            
            volatility_data = {}
            for ticker, data in all_data.items():
                price_data = data.get('price_data')
                if price_data is not None and not price_data.empty:
                    cols = price_data.columns.str.lower()
                    price_data.columns = cols
                    returns = DataFetcher.calculate_returns(price_data['close']).dropna()
                    volatility = DataFetcher.calculate_volatility(returns)
                    volatility_data[ticker] = volatility * 100
            
            if volatility_data:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=list(volatility_data.keys()),
                    y=list(volatility_data.values()),
                    marker_color='#003366',
                    text=[f"{v:.1f}%" for v in volatility_data.values()],
                    textposition="auto",
                ))
                
                fig.update_layout(
                    title="Annualized Volatility (3-Year)",
                    xaxis_title="Company",
                    yaxis_title="Volatility (%)",
                    template="plotly_white",
                    height=400,
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"❌ Error in market analysis: {str(e)}")

# ============================================================================
# TAB 4: RISK ANALYSIS
# ============================================================================

with tab4:
    st.subheader("⚠️ Risk Analysis - All TOP US Tech Companies")
    
    st.info(f"📊 Analyzing risk metrics at {confidence_level}% confidence level")
    
    try:
        all_data = fetch_all_company_data()
        
        if not all_data:
            st.error("❌ Could not fetch data for risk analysis")
        else:
            # Calculate risk metrics for each company
            risk_metrics = []
            
            for ticker, data in all_data.items():
                price_data = data.get('price_data')
                company_info = data.get('company_info', {})
                
                if price_data is not None and not price_data.empty:
                    cols = price_data.columns.str.lower()
                    price_data.columns = cols
                    
                    returns = DataFetcher.calculate_returns(price_data['close']).dropna()
                    annual_return = DataFetcher.calculate_annual_return(price_data['close'])
                    volatility = DataFetcher.calculate_volatility(returns)
                    sharpe = DataFetcher.calculate_sharpe_ratio(returns)
                    max_dd = DataFetcher.calculate_max_drawdown(price_data['close'])
                    
                    risk_metrics.append({
                        'Company': ticker,
                        'Annual Return': f"{annual_return*100:.2f}%",
                        'Volatility': f"{volatility*100:.2f}%",
                        'Sharpe Ratio': f"{sharpe:.2f}",
                        'Max Drawdown': f"{max_dd*100:.2f}%"
                    })
            
            if risk_metrics:
                st.subheader("🎯 Risk Metrics Dashboard")
                df_risk = pd.DataFrame(risk_metrics)
                st.dataframe(df_risk, use_container_width=True)
    
    except Exception as e:
        st.error(f"❌ Error in risk analysis: {str(e)}")

# ============================================================================
# TAB 5: SUMMARY & INSIGHTS
# ============================================================================

with tab5:
    st.subheader("📊 Summary & Key Insights")
    
    try:
        all_data = fetch_all_company_data()
        
        if all_data:
            st.markdown("""
            ### 🏆 Key Highlights
            
            - **Data Source**: Yahoo Finance (yfinance)
            - **Time Period**: 3 Years of daily price data
            - **Companies Analyzed**: 5 Top US Tech Companies
            - **Metrics**: Returns, Volatility, Risk, Financial Metrics
            
            ### 📈 Performance Snapshot
            """)
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            companies = ['NVDA', 'MSFT', 'AAPL', 'GOOGL', 'AMZN']
            
            for idx, (col, ticker) in enumerate(zip([col1, col2, col3, col4, col5], companies)):
                if ticker in all_data:
                    data = all_data[ticker]
                    price_data = data.get('price_data')
                    
                    if price_data is not None and not price_data.empty:
                        cols = price_data.columns.str.lower()
                        price_data.columns = cols
                        
                        annual_return = DataFetcher.calculate_annual_return(price_data['close'])
                        
                        with col:
                            st.metric(
                                ticker,
                                f"{annual_return*100:.1f}%",
                                delta=f"{annual_return*100:.1f}%"
                            )
    
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 12px; padding: 20px;">
    <p><strong>The Mountain Path - World of Finance</strong></p>
    <p>Prof. V. Ravichandran | 28+ Years Corporate Finance & Banking | 10+ Years Academic Excellence</p>
    <p style="color: #999; margin-top: 10px;">Educational Purpose Only • Data from Yahoo Finance</p>
</div>
""", unsafe_allow_html=True)
