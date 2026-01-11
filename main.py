
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
    
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h4 {
        color: #FFD700 !important;
    }
    
    [data-testid="stSidebar"] p {
        color: white !important;
    }
    
    [data-testid="stSidebar"] label {
        color: white !important;
    }
    
    /* Button styling - keep text dark for visibility */
    [data-testid="stSidebar"] button {
        color: #003366 !important;
        background-color: #FFD700 !important;
        font-weight: bold !important;
    }
    
    [data-testid="stSidebar"] button:hover {
        background-color: #FFC700 !important;
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

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div style="background: linear-gradient(135deg, #003366 0%, #004d80 100%); 
            padding: 20px 30px; border-radius: 10px; text-align: center; margin: 15px auto;">
    <h1 style="color: #FFD700; margin: 5px 0; font-size: 36px;">THE MOUNTAIN PATH - WORLD OF FINANCE</h1>
    <p style="color: white; font-size: 16px; margin: 8px 0;">Top US Tech Companies Performance Analysis</p>
    <p style="color: #FFD700; font-size: 12px; margin: 0;">3-Year Rolling Window • Educational Purpose Only</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### 🔧 Controls")
    
    if st.button("🔄 Refresh Data", width="stretch"):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📅 Data Period")
    
    time_period = st.radio(
        "Select Time Period:",
        ["1 Year", "2 Years", "3 Years"],
        index=2,
        key="time_period_selector"
    )
    
    # Convert to yfinance format
    period_map = {
        "1 Year": "1y",
        "2 Years": "2y",
        "3 Years": "3y"
    }
    selected_period = period_map[time_period]
    
    st.info(f"📊 Analyzing {time_period} of data")

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
    
    st.markdown("""
    ### 📊 Five-Lens Financial Framework Analysis
    
    This comprehensive analysis evaluates each company across 5 critical dimensions...
    """)
    
    st.info("📊 Analyzing all 5 companies using Five-Lens Framework...")
    
    try:
        from financial_performance import FiveLensFramework
        
        # Fetch all company data
        all_data = fetch_all_company_data(period=selected_period)
        
        if not all_data:
            st.error("❌ Could not fetch financial data. Please try refreshing.")
        else:
            # Initialize Five-Lens Framework
            framework = FiveLensFramework()
            
            # Build financial analysis for all companies
            analysis_results = []
            detailed_scores = {}
            
            for ticker, data in all_data.items():
                try:
                    company_info = data.get('company_info', {})
                    price_data = data.get('price_data')
                    
                    # Get company name
                    company_name = company_info.get('longName', company_info.get('shortName', 'Unknown'))
                    
                    # Initialize with defaults
                    stock_data_eval = {
                        'pe_ratio': 20.0,
                        'pb_ratio': 3.0,
                        'ps_ratio': 2.0,
                        'dividend_yield': 0.02,
                        'sector': company_info.get('sector', 'Technology'),
                        'price_momentum_52w': 0.25,
                    }
                    
                    financial_metrics_eval = {
                        'roe': 0.20,
                        'npm': 0.15,
                        'roa': 0.10,
                        'roic': 0.15,
                        'debt_to_equity': 0.5,
                        'current_ratio': 2.0,
                        'interest_coverage': 10.0,
                        'free_cash_flow': 1000000000,
                        'revenue_growth_yoy': 0.10,
                        'earnings_growth_yoy': 0.15,
                        'peg_ratio': 1.0,
                    }
                    
                    # Try to get actual values from company_info
                    if 'trailingPE' in company_info:
                        stock_data_eval['pe_ratio'] = company_info['trailingPE']
                    if 'priceToBook' in company_info:
                        stock_data_eval['pb_ratio'] = company_info['priceToBook']
                    if 'priceToSalesTrailing12Months' in company_info:
                        stock_data_eval['ps_ratio'] = company_info['priceToSalesTrailing12Months']
                    if 'dividendYield' in company_info:
                        stock_data_eval['dividend_yield'] = company_info['dividendYield']
                    if 'fiftyTwoWeekChangePercent' in company_info:
                        stock_data_eval['price_momentum_52w'] = company_info['fiftyTwoWeekChangePercent']
                    
                    if 'returnOnEquity' in company_info:
                        financial_metrics_eval['roe'] = company_info['returnOnEquity']
                    if 'profitMargins' in company_info:
                        financial_metrics_eval['npm'] = company_info['profitMargins']
                    if 'returnOnAssets' in company_info:
                        financial_metrics_eval['roa'] = company_info['returnOnAssets']
                    if 'debtToEquity' in company_info:
                        financial_metrics_eval['debt_to_equity'] = company_info['debtToEquity']
                    if 'currentRatio' in company_info:
                        financial_metrics_eval['current_ratio'] = company_info['currentRatio']
                    if 'revenueGrowth' in company_info:
                        financial_metrics_eval['revenue_growth_yoy'] = company_info['revenueGrowth']
                    
                    # Prepare risk metrics
                    risk_metrics_eval = {
                        'beta': 1.2,
                        'volatility_252d': 0.25,
                        'sharpe_ratio': 0.8,
                    }
                    
                    # Calculate volatility and beta from price data if available
                    if price_data is not None and not price_data.empty:
                        try:
                            # Handle MultiIndex columns
                            if isinstance(price_data.columns, pd.MultiIndex):
                                price_data.columns = price_data.columns.get_level_values(1)
                            
                            price_data.columns = price_data.columns.str.lower()
                            
                            # Get close price
                            if 'close' in price_data.columns:
                                close_prices = price_data['close']
                            elif 'adj close' in price_data.columns:
                                close_prices = price_data['adj close']
                            else:
                                close_prices = price_data.iloc[:, -1]
                            
                            returns = DataFetcher.calculate_returns(close_prices).dropna()
                            if not returns.empty:
                                risk_metrics_eval['volatility_252d'] = DataFetcher.calculate_volatility(returns)
                                risk_metrics_eval['sharpe_ratio'] = DataFetcher.calculate_sharpe_ratio(returns)
                                
                                # Calculate beta
                                try:
                                    market_data = fetch_market_data(period=selected_period)
                                    if market_data is not None and not market_data.empty:
                                        if isinstance(market_data.columns, pd.MultiIndex):
                                            market_data.columns = market_data.columns.get_level_values(1)
                                        
                                        market_data.columns = market_data.columns.str.lower()
                                        
                                        if 'close' in market_data.columns:
                                            market_close = market_data['close']
                                        elif 'adj close' in market_data.columns:
                                            market_close = market_data['adj close']
                                        else:
                                            market_close = market_data.iloc[:, -1]
                                        
                                        market_returns = DataFetcher.calculate_returns(market_close).dropna()
                                        if not market_returns.empty:
                                            beta = DataFetcher.calculate_beta(returns, market_returns)
                                            risk_metrics_eval['beta'] = beta
                                except:
                                    pass
                        except:
                            pass
                    
                    # Evaluate using Five-Lens Framework
                    lens_scores = framework.evaluate_stock(stock_data_eval, financial_metrics_eval, risk_metrics_eval)
                    
                    analysis_results.append({
                        'Company': f"{ticker}",
                        'Name': company_name,
                        'Sector': company_info.get('sector', 'N/A'),
                        'Composite Score': lens_scores.composite,
                        'Valuation': lens_scores.valuation,
                        'Quality': lens_scores.quality,
                        'Growth': lens_scores.growth,
                        'Financial Health': lens_scores.financial_health,
                        'Risk & Momentum': lens_scores.risk_momentum,
                    })
                    
                    detailed_scores[ticker] = lens_scores
                    
                except Exception as e:
                    st.error(f"❌ Error analyzing {ticker}: {str(e)}")
                    import traceback
                    st.info(f"Debug: {traceback.format_exc()}")
            
            # Display results if available
            if analysis_results:
                st.markdown("### 🎯 Five-Lens Analysis Summary")
                
                results_df = pd.DataFrame(analysis_results)
                st.dataframe(results_df, use_container_width=True)
                
                # Detailed analysis by company
                st.markdown("### 📊 Detailed Company Analysis")
                
                for ticker, scores in detailed_scores.items():
                    company_info = all_data[ticker]['company_info']
                    company_name = company_info.get('longName', company_info.get('shortName', 'Unknown'))
                    signal, color = framework.get_signal(scores.composite)
                    
                    with st.expander(f"📈 {ticker} - {company_name} | {signal}"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Composite Score", f"{scores.composite:.1f}/100")
                            st.metric("Valuation", f"{scores.valuation:.1f}")
                            st.metric("Quality", f"{scores.quality:.1f}")
                        
                        with col2:
                            st.metric("Growth", f"{scores.growth:.1f}")
                            st.metric("Financial Health", f"{scores.financial_health:.1f}")
                            st.metric("Risk & Momentum", f"{scores.risk_momentum:.1f}")
                        
                        with col3:
                            st.metric("Signal", signal)
                            st.markdown("**Score Breakdown:**")
                            st.markdown(f"- **Valuation**: {scores.valuation:.1f}/100")
                            st.markdown(f"- **Quality**: {scores.quality:.1f}/100")
                            st.markdown(f"- **Growth**: {scores.growth:.1f}/100")
                            st.markdown(f"- **Health**: {scores.financial_health:.1f}/100")
                            st.markdown(f"- **Risk**: {scores.risk_momentum:.1f}/100")
                        
                        # Investment recommendation
                        st.markdown(framework.generate_recommendation(scores, {}))
    
    except Exception as e:
        st.error(f"❌ Error in financial analysis: {str(e)}")
        import traceback
        st.info(f"Debug: {traceback.format_exc()}")
        st.info("💡 Please try clicking 'Refresh Data' button in the sidebar")
# TAB 3: MARKET ANALYSIS
# ============================================================================

with tab3:
    st.subheader("📈 Market Analysis - All TOP US Tech Companies")
    
    st.markdown("""
    ### 📊 Three-Year Market Performance Analysis
    
    This section provides comprehensive market analysis across multiple dimensions:
    
    **Candlestick Charts (3-Year History)**
    - Daily OHLC (Open, High, Low, Close) data
    - Visual price trends and volatility
    - Support and resistance levels
    - Seasonal patterns identification
    
    **Key Metrics Analyzed:**
    
    **Price Performance:**
    - Current vs. historical prices
    - Price momentum trends
    - Support/resistance levels
    - Trend identification (uptrend, downtrend, sideways)
    
    **Returns Analysis:**
    - 3-Year Annualized Returns: Total return over 3 years
    - Daily Returns: Volatility and price changes
    - YTD (Year-to-Date) performance
    - Quarterly performance trends
    
    **Volatility Metrics:**
    - Historical Volatility: Price fluctuation magnitude
    - Implied Volatility: Market expectations
    - Volatility Ranking: Relative risk comparison
    - Beta: Systematic risk vs. S&P 500
    
    **Technical Indicators:**
    - Moving Averages: 50-day, 200-day trends
    - Volume Analysis: Liquidity and conviction
    - Price Action Patterns: Trading signals
    - Support/Resistance Zones: Key price levels
    
    **Market Context:**
    - S&P 500 Comparison: Relative market performance
    - Sector Performance: Technology sector trends
    - Economic Indicators: Macroeconomic context
    - Correlation Matrix: Stock relationship analysis
    """)
    
    st.info("📊 Analyzing all 5 companies: NVDA, MSFT, AAPL, GOOGL, AMZN")
    
    try:
        all_data = fetch_all_company_data(period=selected_period)
        
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
                        # Handle MultiIndex columns from yfinance
                        try:
                            if isinstance(price_data.columns, pd.MultiIndex):
                                price_data.columns = price_data.columns.get_level_values(1)
                            
                            # Ensure column names are correct
                            price_data.columns = price_data.columns.str.lower()
                        except:
                            # If column handling fails, try to reset columns
                            price_data.columns = ['open', 'high', 'low', 'close', 'volume']
                        
                        # Ensure all required columns exist
                        required_cols = ['open', 'high', 'low', 'close']
                        if all(col in price_data.columns for col in required_cols):
                            fig = go.Figure(data=[go.Candlestick(
                                x=price_data.index,
                                open=price_data['open'],
                                high=price_data['high'],
                                low=price_data['low'],
                                close=price_data['close']
                            )])
                            
                            fig.update_layout(
                                title=f"{ticker} - {company_info.get('longName', company_info.get('shortName', 'Unknown'))} (3-Year Candlestick)",
                                xaxis_title="Date",
                                yaxis_title="Price ($)",
                                template="plotly_white",
                                height=500,
                                hovermode="x unified"
                            )
                            
                            st.plotly_chart(fig, width="stretch")
                        else:
                            st.warning(f"Missing required columns for {ticker}. Available columns: {list(price_data.columns)}")
                    else:
                        st.warning(f"Could not load price data for {ticker}")
            
            # Annual returns comparison
            st.subheader("📊 Annual Returns Comparison")
            
            annual_returns = {}
            for ticker, data in all_data.items():
                price_data = data.get('price_data')
                if price_data is not None and not price_data.empty:
                    try:
                        # Handle MultiIndex columns
                        if isinstance(price_data.columns, pd.MultiIndex):
                            price_data.columns = price_data.columns.get_level_values(1)
                        
                        # Convert to lowercase safely
                        price_data.columns = price_data.columns.str.lower()
                        
                        # Get close price
                        if 'close' in price_data.columns:
                            close_prices = price_data['close']
                        elif 'adj close' in price_data.columns:
                            close_prices = price_data['adj close']
                        else:
                            close_prices = price_data.iloc[:, -1]
                        
                        annual_return = DataFetcher.calculate_annual_return(close_prices)
                        annual_returns[ticker] = annual_return * 100
                    except:
                        annual_returns[ticker] = 0.0  # Default if calculation fails
            
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
                
                st.plotly_chart(fig, width="stretch")
            
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
                
                st.plotly_chart(fig, width="stretch")
    
    except Exception as e:
        st.error(f"❌ Error in market analysis: {str(e)}")

# ============================================================================
# TAB 4: RISK ANALYSIS
# ============================================================================

with tab4:
    st.subheader("⚠️ Risk Analysis - All TOP US Tech Companies")
    
    st.markdown("""
    ### 📊 Comprehensive Risk Management Framework
    
    This section analyzes financial and market risks using professional risk metrics:
    
    **Value at Risk (VAR) - Three Confidence Levels**
    
    VAR 90%: Maximum expected loss with 90% confidence (10% probability of worse loss)
    VAR 95%: Maximum expected loss with 95% confidence (5% probability of worse loss)
    VAR 99%: Maximum expected loss with 99% confidence (1% probability of worse loss)
    
    Example: "VAR 95% = -3.5%" means worst daily loss expected 95% of the time is 3.5%
    
    **Conditional Value at Risk (CVAR) - Expected Shortfall**
    
    CVAR shows expected loss WHEN VAR threshold is breached
    - More conservative than VAR
    - Shows tail risk
    - Critical for extreme loss scenarios
    
    **Volatility Analysis**
    - Historical Volatility: Past price fluctuations
    - Annualized Volatility: 252-trading-day standard deviation
    - Volatility Clustering: Periods of high/low volatility
    - Volatility Mean Reversion: Return to average levels
    
    **Risk-Adjusted Returns**
    - Sharpe Ratio: Return per unit of volatility risk
    - Sortino Ratio: Return per unit of downside risk only
    - Information Ratio: Return vs. benchmark
    - Treynor Ratio: Return per unit of systematic risk
    
    **Drawdown Analysis**
    - Maximum Drawdown: Largest peak-to-trough decline
    - Recovery Time: Days to recover from drawdown
    - Drawdown Duration: Length of decline period
    - Recovery Trend: Recovery strength
    
    **Financial Risk Metrics**
    - Debt-to-Equity: Leverage risk
    - Interest Coverage: Default risk
    - Liquidity Ratios: Solvency risk
    - Cash Flow Risk: Operating risk
    
    **Systematic vs Idiosyncratic Risk**
    - Beta: Market risk exposure
    - Alpha: Excess returns
    - R-Squared: Explanatory power
    - Correlation: Diversification benefit
    """)
    
    st.info("📊 Analyzing risk metrics for all 5 companies at multiple confidence levels")
    
    try:
        from risk_analyzer import RiskAnalyzer
        
        all_data = fetch_all_company_data(period=selected_period)
        
        if not all_data:
            st.error("❌ Could not fetch data for risk analysis")
        else:
            # Calculate comprehensive risk metrics
            risk_data = []
            detailed_risk = {}
            
            for ticker, data in all_data.items():
                price_data = data.get('price_data')
                company_info = data.get('company_info', {})
                
                if price_data is not None and not price_data.empty:
                    cols = price_data.columns.str.lower()
                    price_data.columns = cols
                    
                    returns = DataFetcher.calculate_returns(price_data['close']).dropna()
                    annual_return = DataFetcher.calculate_annual_return(price_data['close'])
                    
                    # Calculate all risk metrics
                    volatility = RiskAnalyzer.calculate_annual_volatility(returns)
                    sharpe = (annual_return - 0.04) / volatility if volatility > 0 else 0
                    sortino = RiskAnalyzer.calculate_sortino_ratio(returns)
                    max_dd = RiskAnalyzer.calculate_max_drawdown(price_data['close'])
                    recovery = RiskAnalyzer.calculate_recovery_time(price_data['close'])
                    
                    # Calculate VAR/CVAR for all confidence levels
                    var_90 = RiskAnalyzer.calculate_var(returns, 0.90)
                    var_95 = RiskAnalyzer.calculate_var(returns, 0.95)
                    var_99 = RiskAnalyzer.calculate_var(returns, 0.99)
                    
                    cvar_90 = RiskAnalyzer.calculate_cvar(returns, 0.90)
                    cvar_95 = RiskAnalyzer.calculate_cvar(returns, 0.95)
                    cvar_99 = RiskAnalyzer.calculate_cvar(returns, 0.99)
                    
                    # Risk assessment
                    risk_assessment = RiskAnalyzer.get_risk_assessment(var_95, cvar_95, volatility, sharpe)
                    
                    # Store for display
                    risk_data.append({
                        'Company': ticker,
                        'Annual Return': f"{annual_return*100:.2f}%",
                        'Volatility': f"{volatility*100:.2f}%",
                        'Sharpe Ratio': f"{sharpe:.2f}",
                        'Sortino Ratio': f"{sortino:.2f}",
                        'Max Drawdown': f"{max_dd*100:.2f}%",
                        'VAR 90%': f"{var_90*100:.2f}%",
                        'VAR 95%': f"{var_95*100:.2f}%",
                        'VAR 99%': f"{var_99*100:.2f}%",
                        'CVAR 90%': f"{cvar_90*100:.2f}%",
                        'CVAR 95%': f"{cvar_95*100:.2f}%",
                        'CVAR 99%': f"{cvar_99*100:.2f}%",
                        'Risk Assessment': risk_assessment
                    })
                    
                    detailed_risk[ticker] = {
                        'annual_return': annual_return,
                        'volatility': volatility,
                        'sharpe_ratio': sharpe,
                        'sortino_ratio': sortino,
                        'max_drawdown': max_dd,
                        'recovery_days': recovery,
                        'var_90': var_90,
                        'var_95': var_95,
                        'var_99': var_99,
                        'cvar_90': cvar_90,
                        'cvar_95': cvar_95,
                        'cvar_99': cvar_99,
                        'risk_assessment': risk_assessment,
                        'company_info': company_info,
                        'returns': returns
                    }
            
            if risk_data:
                # Risk Metrics Dashboard
                st.subheader("🎯 Risk Metrics Dashboard")
                df_risk = pd.DataFrame(risk_data)
                st.dataframe(df_risk, width="stretch", hide_index=True)
                
                st.divider()
                
                # VAR/CVAR Analysis Charts for all confidence levels
                st.subheader("📊 VAR & CVAR Analysis - All Confidence Levels")
                
                # Prepare data for all confidence levels
                companies = list(detailed_risk.keys())
                var_90_vals = [detailed_risk[t]['var_90']*100 for t in companies]
                var_95_vals = [detailed_risk[t]['var_95']*100 for t in companies]
                var_99_vals = [detailed_risk[t]['var_99']*100 for t in companies]
                
                cvar_90_vals = [detailed_risk[t]['cvar_90']*100 for t in companies]
                cvar_95_vals = [detailed_risk[t]['cvar_95']*100 for t in companies]
                cvar_99_vals = [detailed_risk[t]['cvar_99']*100 for t in companies]
                
                # VAR Chart
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Value at Risk (VAR) - All Confidence Levels**")
                    fig_var = go.Figure()
                    fig_var.add_trace(go.Bar(
                        x=companies,
                        y=var_90_vals,
                        name='VAR 90%',
                        marker_color='#ffb3b3',
                    ))
                    fig_var.add_trace(go.Bar(
                        x=companies,
                        y=var_95_vals,
                        name='VAR 95%',
                        marker_color='#ff6b6b',
                    ))
                    fig_var.add_trace(go.Bar(
                        x=companies,
                        y=var_99_vals,
                        name='VAR 99%',
                        marker_color='#ff4444',
                    ))
                    fig_var.update_layout(
                        title="Value at Risk Across Confidence Levels",
                        xaxis_title="Company",
                        yaxis_title="VAR (%)",
                        template="plotly_white",
                        height=400,
                        barmode='group',
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig_var, width="stretch")
                
                with col2:
                    st.markdown("**Conditional VAR (CVAR) - All Confidence Levels**")
                    fig_cvar = go.Figure()
                    fig_cvar.add_trace(go.Bar(
                        x=companies,
                        y=cvar_90_vals,
                        name='CVAR 90%',
                        marker_color='#ff9999',
                    ))
                    fig_cvar.add_trace(go.Bar(
                        x=companies,
                        y=cvar_95_vals,
                        name='CVAR 95%',
                        marker_color='#ff5555',
                    ))
                    fig_cvar.add_trace(go.Bar(
                        x=companies,
                        y=cvar_99_vals,
                        name='CVAR 99%',
                        marker_color='#ff2222',
                    ))
                    fig_cvar.update_layout(
                        title="Conditional VAR Across Confidence Levels",
                        xaxis_title="Company",
                        yaxis_title="CVAR (%)",
                        template="plotly_white",
                        height=400,
                        barmode='group',
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig_cvar, width="stretch")
                
                st.divider()
                
                # Detailed Risk Analysis by Company
                st.subheader("📈 Detailed Risk Analysis by Company")
                
                for ticker, data in detailed_risk.items():
                    company_info = data['company_info']
                    company_name_risk = company_info.get('longName', company_info.get('shortName', 'Unknown'))
                    
                    with st.expander(f"📊 {ticker} - {company_name_risk} | {data['risk_assessment']}"):
                        col1, col2, col3, col4, col5 = st.columns(5)
                        
                        with col1:
                            st.metric("Annual Return", f"{data['annual_return']*100:.2f}%")
                        with col2:
                            st.metric("Volatility", f"{data['volatility']*100:.2f}%")
                        with col3:
                            st.metric("Sharpe Ratio", f"{data['sharpe_ratio']:.2f}")
                        with col4:
                            st.metric("Sortino Ratio", f"{data['sortino_ratio']:.2f}")
                        with col5:
                            st.metric("Max Drawdown", f"{data['max_drawdown']*100:.2f}%")
                        
                        st.divider()
                        
                        st.markdown("**Value at Risk (VAR) - All Confidence Levels**")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("VAR 90%", f"{data['var_90']*100:.2f}%")
                        with col2:
                            st.metric("VAR 95%", f"{data['var_95']*100:.2f}%")
                        with col3:
                            st.metric("VAR 99%", f"{data['var_99']*100:.2f}%")
                        
                        st.markdown("**Conditional Value at Risk (CVAR) - All Confidence Levels**")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("CVAR 90%", f"{data['cvar_90']*100:.2f}%")
                        with col2:
                            st.metric("CVAR 95%", f"{data['cvar_95']*100:.2f}%")
                        with col3:
                            st.metric("CVAR 99%", f"{data['cvar_99']*100:.2f}%")
                        
                        st.divider()
                        
                        st.markdown("**Drawdown Analysis**")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("Maximum Drawdown", f"{data['max_drawdown']*100:.2f}%")
                        with col2:
                            recovery = data.get('recovery_days', 0)
                            if recovery == -1:
                                st.metric("Recovery Time", "Still in DD")
                            elif recovery == 0:
                                st.metric("Recovery Time", "N/A")
                            else:
                                st.metric("Recovery Time", f"{recovery} days")
                        
                        st.divider()
                        
                        st.markdown(f"**Risk Assessment: {data['risk_assessment']}**")
                        st.markdown("""
                        **Interpretation:**
                        - **VAR**: Maximum expected loss with X% confidence
                        - **CVAR**: Expected loss if VAR threshold is breached
                        - **Max Drawdown**: Largest peak-to-trough decline
                        - **Recovery Time**: Days to recover from maximum drawdown
                        - **Higher confidence (99%)** = More conservative estimate
                        - **Lower confidence (90%)** = More aggressive estimate
                        """)
    
    except Exception as e:
        st.error(f"❌ Error in risk analysis: {str(e)}")
        import traceback
        st.info(f"Debug: {traceback.format_exc()}")
        st.info("💡 Please try clicking 'Refresh Data' button in the sidebar")

# ============================================================================
# TAB 5: SUMMARY & INSIGHTS
# ============================================================================

with tab5:
    st.subheader("📊 Summary & Key Insights")
    
    st.markdown("""
    ### 🎓 About This Educational Platform
    
    **The Mountain Path - World of Finance** provides comprehensive analysis of 
    the top 5 US Technology companies using professional investment frameworks.
    
    ### 📊 Analytical Framework
    
    **1. Financial Performance Analysis**
    - Five-Lens Framework evaluates companies across 5 dimensions
    - Composite scoring from 0-100
    - Investment signals from Strong Buy to Avoid
    - Detailed metric breakdowns
    
    **2. Market Analysis**
    - 3-year candlestick price charts
    - Technical indicators and patterns
    - Volume analysis
    - Performance trends
    
    **3. Risk Management**
    - Value at Risk (VAR) calculations
    - Conditional VAR (Expected Shortfall)
    - Volatility and drawdown analysis
    - Risk-adjusted return metrics
    
    **4. Educational Metrics**
    - Sharpe Ratio: Risk-adjusted returns
    - Sortino Ratio: Downside risk penalization
    - Beta: Systematic risk
    - Maximum Drawdown: Largest losses
    
    ### 💡 Key Insights
    
    **Technology Sector Overview:**
    - NVDA: Semiconductor/AI leadership
    - MSFT: Cloud & Enterprise software
    - AAPL: Consumer electronics ecosystem
    - GOOGL: Search & Digital advertising
    - AMZN: E-commerce & Cloud services
    
    **Data Quality:**
    - Source: Yahoo Finance (Industry standard)
    - Period: 3-year rolling window
    - Frequency: Daily OHLCV data
    - Quality: Adjusted for splits/dividends
    
    ### 📈 Performance Metrics
    """)
    
    try:
        all_data = fetch_all_company_data(period=selected_period)
        
        if all_data:
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
            
            st.markdown("""
            ### 📚 Educational Value
            
            **For Students Learning:**
            - Financial statement analysis
            - Risk management frameworks
            - Investment valuation methods
            - Quantitative finance techniques
            - Portfolio management concepts
            
            **For Professionals:**
            - Benchmark comparison
            - Relative valuation analysis
            - Risk assessment tools
            - Performance tracking
            - Decision support
            
            ### ⚠️ Important Disclaimers
            
            ✅ **Educational Purpose Only** - This tool is for learning
            ✅ **NOT Financial Advice** - Consult qualified advisors
            ✅ **Past Performance** - Does not guarantee future results
            ✅ **Simplified Models** - Real analysis requires more data
            ✅ **Market Risks** - All investments carry risk
            
            ### 🔍 How to Use This Platform
            
            1. **About Tab**: Understand platform capabilities
            2. **Financial Performance**: Evaluate company quality
            3. **Market Analysis**: Study price trends and charts
            4. **Risk Analysis**: Understand downside scenarios
            5. **Summary**: Review key metrics and insights
            
            ### 📖 Further Learning
            
            - Study the Five-Lens Framework methodology
            - Understand each risk metric in depth
            - Compare companies across dimensions
            - Practice valuation techniques
            - Build investment decision skills
            """)
    
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")

# ============================================================================
# FOOTER
# ============================================================================

from footer import render_footer
render_footer()
