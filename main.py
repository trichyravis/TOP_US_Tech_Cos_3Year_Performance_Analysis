
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
    
    st.info("📊 Analyzing all 5 companies using Five-Lens Framework...")
    
    try:
        from financial_performance import FiveLensFramework
        
        # Fetch all company data
        all_data = fetch_all_company_data()
        
        if not all_data:
            st.error("❌ Could not fetch financial data. Please try refreshing.")
        else:
            # Initialize Five-Lens Framework
            framework = FiveLensFramework()
            
            # Build financial analysis for all companies
            analysis_results = []
            detailed_scores = {}
            
            for ticker, data in all_data.items():
                company_info = data.get('company_info', {})
                info = data.get('info', {})
                price_data = data.get('price_data')
                
                # Prepare stock data for Five-Lens evaluation
                stock_data_eval = {
                    'pe_ratio': info.get('trailingPE'),
                    'pb_ratio': info.get('priceToBook'),
                    'ps_ratio': info.get('priceToSalesTrailing12Months'),
                    'dividend_yield': info.get('dividendYield') or 0,
                    'sector': company_info.get('sector', 'Technology'),
                    'price_momentum_52w': info.get('fiftyTwoWeekChangePercent'),
                }
                
                # Prepare financial metrics
                financial_metrics_eval = {
                    'roe': info.get('returnOnEquity'),
                    'npm': info.get('profitMargins'),
                    'roa': info.get('returnOnAssets'),
                    'roic': info.get('returnOnCapital'),
                    'debt_to_equity': info.get('debtToEquity'),
                    'current_ratio': info.get('currentRatio'),
                    'interest_coverage': info.get('interestCoverage') or 10.0,
                    'free_cash_flow': info.get('freeCashFlow'),
                    'revenue_growth_yoy': info.get('revenueGrowth'),
                    'earnings_growth_yoy': info.get('earningsGrowth'),
                    'peg_ratio': info.get('pegRatio'),
                }
                
                # Prepare risk metrics
                risk_metrics_eval = {
                    'beta': DataFetcher.STOCK_BETA.get(ticker, 1.0),
                    'volatility_252d': 0.25,  # Default, can be calculated from price_data
                    'sharpe_ratio': 0.8,  # Default
                }
                
                # Calculate volatility from price data if available
                if price_data is not None and not price_data.empty:
                    cols = price_data.columns.str.lower()
                    price_data.columns = cols
                    returns = DataFetcher.calculate_returns(price_data['close']).dropna()
                    if not returns.empty:
                        risk_metrics_eval['volatility_252d'] = DataFetcher.calculate_volatility(returns)
                        risk_metrics_eval['sharpe_ratio'] = DataFetcher.calculate_sharpe_ratio(returns)
                
                # Evaluate using Five-Lens Framework
                lens_scores = framework.evaluate_stock(stock_data_eval, financial_metrics_eval, risk_metrics_eval)
                
                analysis_results.append({
                    'Company': f"{ticker}",
                    'Name': company_info.get('name', 'Unknown'),
                    'Sector': company_info.get('sector', 'N/A'),
                    'Composite Score': lens_scores.composite,
                    'Valuation': lens_scores.valuation,
                    'Quality': lens_scores.quality,
                    'Growth': lens_scores.growth,
                    'Financial Health': lens_scores.financial_health,
                    'Risk & Momentum': lens_scores.risk_momentum,
                })
                
                detailed_scores[ticker] = {
                    'scores': lens_scores,
                    'company_info': company_info,
                    'info': info,
                    'stock_data': stock_data_eval,
                    'financial_metrics': financial_metrics_eval
                }
            
            # Display Five-Lens Scores Summary
            st.subheader("🎯 Five-Lens Analysis Summary")
            df_analysis = pd.DataFrame(analysis_results)
            
            # Format numeric columns for display
            for col in ['Composite Score', 'Valuation', 'Quality', 'Growth', 'Financial Health', 'Risk & Momentum']:
                if col in df_analysis.columns:
                    df_analysis[col] = df_analysis[col].apply(lambda x: f"{x:.1f}" if isinstance(x, (int, float)) else x)
            
            st.dataframe(df_analysis, use_container_width=True)
            
            # Display individual company analysis
            st.subheader("📊 Detailed Company Analysis")
            
            for ticker, data in detailed_scores.items():
                scores = data['scores']
                company_info = data['company_info']
                info = data['info']
                
                signal, color = framework.get_signal(scores.composite)
                
                with st.expander(f"📈 {ticker} - {company_info.get('name', 'Unknown')} | {signal}"):
                    # Composite Score and Signal
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.metric("Composite Score", f"{scores.composite:.1f}/100", 
                                 delta=f"Signal: {signal.split()[0]}")
                    
                    with col2:
                        st.metric("Sector", company_info.get('sector', 'N/A'))
                    
                    st.divider()
                    
                    # Five Lens Scores Visualization
                    st.markdown("**Five-Lens Scores:**")
                    col1, col2, col3, col4, col5 = st.columns(5)
                    
                    with col1:
                        st.metric("Valuation", f"{scores.valuation:.1f}", delta="")
                    with col2:
                        st.metric("Quality", f"{scores.quality:.1f}", delta="")
                    with col3:
                        st.metric("Growth", f"{scores.growth:.1f}", delta="")
                    with col4:
                        st.metric("Financial Health", f"{scores.financial_health:.1f}", delta="")
                    with col5:
                        st.metric("Risk & Momentum", f"{scores.risk_momentum:.1f}", delta="")
                    
                    st.divider()
                    
                    # Key Financial Data
                    st.markdown("**Key Financial Metrics:**")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        revenue = (info.get('totalRevenue', 0) or 0) / 1e9
                        st.metric("Revenue ($B)", f"${revenue:.1f}")
                    with col2:
                        pe = info.get('trailingPE')
                        st.metric("P/E Ratio", f"{pe:.1f}" if pe else "N/A")
                    with col3:
                        pb = info.get('priceToBook')
                        st.metric("P/B Ratio", f"{pb:.1f}" if pb else "N/A")
                    with col4:
                        roe = info.get('returnOnEquity')
                        if roe:
                            st.metric("ROE", f"{roe*100:.1f}%")
                        else:
                            st.metric("ROE", "N/A")
                    
                    # Investment Recommendation
                    st.markdown(framework.generate_recommendation(scores, data['stock_data']))
    
    except Exception as e:
        st.error(f"❌ Error in financial analysis: {str(e)}")
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
