"""
Main Application File - Streamlit Entry Point
Purpose: Render the complete 5-tab dashboard for US Tech Companies Analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

from config import (
    PAGE_CONFIG, APP_TITLE, TICKERS, COLORS, DISCLAIMER, 
    LINKEDIN_URL, GITHUB_URL, TRADING_DAYS_PER_YEAR
)
from styles import apply_mountain_path_theme, render_header, render_footer
from components import (
    render_company_selector, render_sidebar_header, render_metrics_row,
    render_data_table, render_candlestick_chart
)
from data_handler import (
    initialize_data_handler, get_stock_data, fetch_risk_free_rate
)
from analytics import (
    calculate_returns, calculate_annual_return, calculate_volatility,
    calculate_sharpe_ratio, calculate_sortino_ratio, calculate_var_cvar,
    calculate_max_drawdown, generate_risk_summary
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(**PAGE_CONFIG)
apply_mountain_path_theme()

# Initialize data handler on first run
if 'data_initialized' not in st.session_state:
    initialize_data_handler()
    st.session_state.data_initialized = True
    st.session_state.last_refresh = datetime.now()

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

with st.sidebar:
    render_sidebar_header("Navigation", "📊")
    
    # Refresh data button
    if st.button("🔄 Refresh Data", help="Manually refresh all data (15min cooldown)"):
        st.cache_data.clear()
        st.session_state.last_refresh = datetime.now()
        st.rerun()
    
    st.divider()
    
    # Last refresh time
    if 'last_refresh' in st.session_state:
        st.caption(f"Last refresh: {st.session_state.last_refresh.strftime('%Y-%m-%d %H:%M:%S')}")

# ============================================================================
# MAIN CONTENT
# ============================================================================

render_header()

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 About Platform",
    "💰 Financial Performance",
    "📈 Market Analysis",
    "⚠️ Risk Analysis",
    "📊 Summary & Insights"
])

# ============================================================================
# TAB 1: ABOUT THE PLATFORM
# ============================================================================

with tab1:
    st.subheader("About The Mountain Path - World of Finance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📚 Platform Overview
        
        **The Mountain Path - World of Finance** is an educational platform 
        designed to help students understand:
        - Financial analysis and valuation
        - Investment concepts and strategies
        - Risk management frameworks
        - Quantitative finance techniques
        
        ### 🎯 This Tool
        
        This dashboard provides a comprehensive **3-year performance analysis** 
        of the top US IT companies.
        
        #### Companies Analyzed
        - **NVIDIA** (NVDA) - AI & Semiconductors
        - **Microsoft** (MSFT) - Cloud & Software
        - **Apple** (AAPL) - Consumer Electronics
        - **Alphabet/Google** (GOOGL) - Digital Advertising
        - **Amazon** (AMZN) - E-commerce & Cloud
        """)
    
    with col2:
        st.markdown("""
        ### 🔧 Key Features
        
        ✓ Historical stock price analysis (3 years daily)  
        ✓ Financial performance metrics (Revenue, Income, Margins)  
        ✓ Risk assessment (VaR, CVaR, Sharpe, Sortino, Max Drawdown)  
        ✓ Interactive visualizations (Candlestick, Heatmaps)  
        ✓ Real-time data updates (every 4 hours)  
        ✓ Correlation analysis (5-stock comparison)  
        
        ### 📊 Data Sources
        
        | Source | Data | Update Frequency |
        |--------|------|------------------|
        | Yahoo Finance | Stock Prices (Daily) | Every 4 hours |
        | Yahoo Finance | Financial Data (Annual) | Daily |
        | Federal Reserve (FRED) | 10Y Treasury Yield | Daily |
        """)
    
    st.divider()
    
    # Disclaimer
    st.warning(DISCLAIMER)
    
    st.divider()
    
    st.subheader("📞 Contact & Resources")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        **LinkedIn**  
        [trichyravis]({LINKEDIN_URL})
        """)
    
    with col2:
        st.markdown(f"""
        **GitHub**  
        [trichyravis]({GITHUB_URL})
        """)
    
    with col3:
        st.markdown("""
        **Author**  
        Prof. V. Ravichandran  
        28+ Years Finance & Banking  
        10+ Years Academic Excellence
        """)

# ============================================================================
# TAB 2: FINANCIAL PERFORMANCE
# ============================================================================

with tab2:
    st.subheader("💰 Financial Performance Analysis")
    
    with st.sidebar:
        render_sidebar_header("Filters", "🔍")
        selected_ticker = render_company_selector(mode='single', default='NVDA')
        show_all = st.checkbox("Compare All Companies", value=False)
    
    if show_all:
        st.info("Comparing all 5 companies financial metrics")
        
        try:
            # Fetch financial data for all companies
            financial_data = []
            
            for ticker in TICKERS.keys():
                try:
                    ticker_obj = yf.Ticker(ticker)
                    info = ticker_obj.info
                    
                    financial_data.append({
                        'Company': ticker,
                        'Revenue ($B)': info.get('totalRevenue', 0) / 1e9,
                        'Operating Income ($B)': info.get('operatingIncome', 0) / 1e9,
                        'Net Income ($B)': info.get('netIncome', 0) / 1e9,
                        'Employees': info.get('fullTimeEmployees', 0),
                        'Market Cap ($B)': info.get('marketCap', 0) / 1e9,
                    })
                except Exception as e:
                    st.warning(f"Could not fetch data for {ticker}: {e}")
            
            if financial_data:
                df_financial = pd.DataFrame(financial_data)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Highest Revenue", 
                             f"${df_financial['Revenue ($B)'].max():.1f}B")
                with col2:
                    st.metric("Highest Net Income", 
                             f"${df_financial['Net Income ($B)'].max():.1f}B")
                with col3:
                    st.metric("Largest Market Cap", 
                             f"${df_financial['Market Cap ($B)'].max():.1f}B")
                
                st.subheader("Financial Metrics Comparison")
                render_data_table(df_financial)
        
        except Exception as e:
            st.error(f"Error fetching financial data: {e}")
    
    else:
        st.info(f"Analyzing {selected_ticker} - {TICKERS[selected_ticker]}")
        
        try:
            ticker_obj = yf.Ticker(selected_ticker)
            info = ticker_obj.info
            
            # Display key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                revenue = info.get('totalRevenue', 0) / 1e9
                st.metric("Annual Revenue", f"${revenue:.1f}B")
            
            with col2:
                op_income = info.get('operatingIncome', 0) / 1e9
                st.metric("Operating Income", f"${op_income:.1f}B")
            
            with col3:
                net_income = info.get('netIncome', 0) / 1e9
                st.metric("Net Income", f"${net_income:.1f}B")
            
            with col4:
                market_cap = info.get('marketCap', 0) / 1e9
                st.metric("Market Cap", f"${market_cap:.1f}B")
            
            st.divider()
            
            # Get historical price data for trend
            price_data = get_stock_data(selected_ticker)
            
            if price_data is not None and len(price_data) > 0:
                # Calculate margins
                profit_margin = (net_income / revenue * 100) if revenue > 0 else 0
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Profit Margin", f"{profit_margin:.1f}%")
                with col2:
                    st.metric("Operating Margin", 
                             f"{(op_income/revenue*100):.1f}%" if revenue > 0 else "N/A")
                with col3:
                    st.metric("Employees", f"{info.get('fullTimeEmployees', 0):,.0f}")
                
                st.divider()
                
                # Price trend
                st.subheader("Stock Price Trend (3 Years)")
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=price_data.index,
                    y=price_data['Close'],
                    mode='lines',
                    name='Close Price',
                    line=dict(color=COLORS['primary'], width=2)
                ))
                
                fig.update_layout(
                    title=f"{selected_ticker} Price Trend",
                    xaxis_title="Date",
                    yaxis_title="Price ($)",
                    template="plotly_white",
                    height=400,
                    hovermode="x unified"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(f"Could not fetch price data for {selected_ticker}")
        
        except Exception as e:
            st.error(f"Error fetching data for {selected_ticker}: {e}")

# ============================================================================
# TAB 3: MARKET ANALYSIS
# ============================================================================

with tab3:
    st.subheader("📈 Market Analysis")
    
    with st.sidebar:
        render_sidebar_header("Filters", "🔍")
        selected_tickers = st.multiselect(
            "Select Companies:",
            options=list(TICKERS.keys()),
            default=['NVDA', 'MSFT'],
            format_func=lambda x: f"{x} - {TICKERS[x]}"
        )
    
    if not selected_tickers:
        st.error("Select at least one company")
        st.stop()
    
    st.info(f"Analyzing {', '.join(selected_tickers)}")
    
    try:
        # Get price data
        price_data_dict = {}
        for ticker in selected_tickers:
            data = get_stock_data(ticker)
            if data is not None:
                price_data_dict[ticker] = data
        
        if not price_data_dict:
            st.error("Could not fetch price data for selected companies")
            st.stop()
        
        # Candlestick chart for first selected ticker
        st.subheader(f"Price Movement - {selected_tickers[0]}")
        
        price_data = price_data_dict[selected_tickers[0]]
        
        fig = go.Figure(data=[go.Candlestick(
            x=price_data.index,
            open=price_data['Open'],
            high=price_data['High'],
            low=price_data['Low'],
            close=price_data['Close']
        )])
        
        fig.update_layout(
            title=f"{selected_tickers[0]} - Candlestick Chart (3 Years)",
            xaxis_title="Date",
            yaxis_title="Price ($)",
            template="plotly_white",
            height=500,
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Annual returns comparison
        st.subheader("Annual Returns Comparison")
        
        annual_returns = {}
        for ticker, data in price_data_dict.items():
            annual_return = calculate_annual_return(data['Close'])
            annual_returns[ticker] = annual_return * 100
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=list(annual_returns.keys()),
            y=list(annual_returns.values()),
            marker_color=[COLORS['primary'] if v > 0 else COLORS['error'] 
                         for v in annual_returns.values()]
        ))
        
        fig.update_layout(
            title="3-Year Annualized Returns",
            xaxis_title="Company",
            yaxis_title="Annual Return (%)",
            template="plotly_white",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Volatility comparison
        st.subheader("Annual Volatility Comparison")
        
        volatilities = {}
        for ticker, data in price_data_dict.items():
            returns = calculate_returns(data['Close'])
            vol = calculate_volatility(returns, annualize=True)
            volatilities[ticker] = vol * 100
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=list(volatilities.keys()),
            y=list(volatilities.values()),
            marker_color=COLORS['secondary']
        ))
        
        fig.update_layout(
            title="Annual Volatility (Risk)",
            xaxis_title="Company",
            yaxis_title="Volatility (%)",
            template="plotly_white",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error in market analysis: {e}")

# ============================================================================
# TAB 4: RISK ANALYSIS
# ============================================================================

with tab4:
    st.subheader("⚠️ Risk Analysis")
    
    with st.sidebar:
        render_sidebar_header("Risk Parameters", "⚙️")
        
        selected_tickers = st.multiselect(
            "Select Companies:",
            options=list(TICKERS.keys()),
            default=['NVDA', 'MSFT'],
            format_func=lambda x: f"{x} - {TICKERS[x]}"
        )
        
        confidence = st.radio("VaR Confidence Level:", [90, 95, 99], index=1) / 100
    
    if not selected_tickers:
        st.error("Select at least one company")
        st.stop()
    
    st.info(f"Analyzing risk metrics for {', '.join(selected_tickers)} at {int(confidence*100)}% confidence")
    
    try:
        rf_rate = fetch_risk_free_rate()
        
        # Generate risk summaries
        risk_summaries = []
        
        for ticker in selected_tickers:
            data = get_stock_data(ticker)
            if data is not None:
                returns = calculate_returns(data['Close'])
                summary = generate_risk_summary(ticker, data['Close'], returns, rf_rate)
                risk_summaries.append(summary)
        
        if risk_summaries:
            # Risk metrics table
            st.subheader("Risk Metrics Dashboard")
            
            risk_df = pd.DataFrame(risk_summaries)
            
            # Format for display
            risk_df_display = risk_df.copy()
            risk_df_display['annual_return'] = risk_df_display['annual_return'].apply(lambda x: f"{x*100:.2f}%")
            risk_df_display['annual_volatility'] = risk_df_display['annual_volatility'].apply(lambda x: f"{x*100:.2f}%")
            risk_df_display['sharpe_ratio'] = risk_df_display['sharpe_ratio'].apply(lambda x: f"{x:.2f}")
            risk_df_display['sortino_ratio'] = risk_df_display['sortino_ratio'].apply(lambda x: f"{x:.2f}")
            risk_df_display['max_drawdown'] = risk_df_display['max_drawdown'].apply(lambda x: f"{x*100:.2f}%")
            risk_df_display['var_95'] = risk_df_display['var_95'].apply(lambda x: f"{x*100:.2f}%")
            risk_df_display['cvar_95'] = risk_df_display['cvar_95'].apply(lambda x: f"{x*100:.2f}%")
            
            # Select columns to display
            display_cols = ['ticker', 'annual_return', 'annual_volatility', 'sharpe_ratio', 'sortino_ratio', 'max_drawdown']
            render_data_table(risk_df_display[display_cols])
            
            st.divider()
            
            # Key metrics highlights
            st.subheader("Risk Metrics Highlights")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                best_sharpe_idx = risk_df['sharpe_ratio'].idxmax()
                best_sharpe_ticker = risk_df.loc[best_sharpe_idx, 'ticker']
                best_sharpe = risk_df.loc[best_sharpe_idx, 'sharpe_ratio']
                st.metric("Best Risk-Adjusted Return (Sharpe)", 
                         f"{best_sharpe_ticker}", f"{best_sharpe:.2f}")
            
            with col2:
                best_sortino_idx = risk_df['sortino_ratio'].idxmax()
                best_sortino_ticker = risk_df.loc[best_sortino_idx, 'ticker']
                best_sortino = risk_df.loc[best_sortino_idx, 'sortino_ratio']
                st.metric("Best Downside Risk (Sortino)", 
                         f"{best_sortino_ticker}", f"{best_sortino:.2f}")
            
            with col3:
                lowest_vol_idx = risk_df['annual_volatility'].idxmin()
                lowest_vol_ticker = risk_df.loc[lowest_vol_idx, 'ticker']
                lowest_vol = risk_df.loc[lowest_vol_idx, 'annual_volatility']
                st.metric("Lowest Volatility", 
                         f"{lowest_vol_ticker}", f"{lowest_vol*100:.1f}%")
            
            with col4:
                min_dd_idx = risk_df['max_drawdown'].idxmax()  # Highest (least negative)
                min_dd_ticker = risk_df.loc[min_dd_idx, 'ticker']
                min_dd = risk_df.loc[min_dd_idx, 'max_drawdown']
                st.metric("Smallest Max Drawdown", 
                         f"{min_dd_ticker}", f"{min_dd*100:.1f}%")
            
            st.divider()
            
            # VaR visualization
            st.subheader(f"Value-at-Risk (VaR) at {int(confidence*100)}% Confidence")
            
            var_data = risk_df[['ticker', 'var_95']].copy()
            var_data['var_95'] = var_data['var_95'] * 100
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=var_data['ticker'],
                y=var_data['var_95'],
                marker_color=COLORS['error']
            ))
            
            fig.update_layout(
                title=f"Daily Value-at-Risk ({int(confidence*100)}% confidence)",
                xaxis_title="Company",
                yaxis_title="Daily VaR (%)",
                template="plotly_white",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error in risk analysis: {e}")

# ============================================================================
# TAB 5: SUMMARY & INSIGHTS
# ============================================================================

with tab5:
    st.subheader("📊 Executive Summary & Insights")
    
    try:
        # Get data for all companies
        all_price_data = {}
        all_summaries = []
        
        rf_rate = fetch_risk_free_rate()
        
        for ticker in TICKERS.keys():
            try:
                data = get_stock_data(ticker)
                if data is not None:
                    all_price_data[ticker] = data
                    returns = calculate_returns(data['Close'])
                    summary = generate_risk_summary(ticker, data['Close'], returns, rf_rate)
                    all_summaries.append(summary)
            except Exception as e:
                st.warning(f"Could not analyze {ticker}: {e}")
        
        if all_summaries:
            summary_df = pd.DataFrame(all_summaries)
            
            # Key insights
            st.subheader("🎯 Key Insights")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                best_return_idx = summary_df['annual_return'].idxmax()
                best_return_ticker = summary_df.loc[best_return_idx, 'ticker']
                best_return = summary_df.loc[best_return_idx, 'annual_return']
                st.metric("🚀 Best Performer (Return)", 
                         f"{best_return_ticker}", f"{best_return*100:.1f}%")
            
            with col2:
                highest_growth_idx = summary_df['annual_return'].idxmax()
                st.metric("📈 Highest Growth Company", 
                         f"{summary_df.loc[highest_growth_idx, 'ticker']}", 
                         f"{summary_df.loc[highest_growth_idx, 'annual_return']*100:.1f}%")
            
            with col3:
                lowest_volatility_idx = summary_df['annual_volatility'].idxmin()
                st.metric("🛡️ Most Stable (Lowest Vol)", 
                         f"{summary_df.loc[lowest_volatility_idx, 'ticker']}", 
                         f"{summary_df.loc[lowest_volatility_idx, 'annual_volatility']*100:.1f}%")
            
            st.divider()
            
            # Comprehensive comparison table
            st.subheader("📋 Complete Metrics Comparison (All Companies)")
            
            summary_df_display = summary_df.copy()
            summary_df_display['annual_return'] = summary_df_display['annual_return'].apply(lambda x: f"{x*100:.2f}%")
            summary_df_display['annual_volatility'] = summary_df_display['annual_volatility'].apply(lambda x: f"{x*100:.2f}%")
            summary_df_display['sharpe_ratio'] = summary_df_display['sharpe_ratio'].apply(lambda x: f"{x:.2f}")
            summary_df_display['sortino_ratio'] = summary_df_display['sortino_ratio'].apply(lambda x: f"{x:.2f}")
            summary_df_display['max_drawdown'] = summary_df_display['max_drawdown'].apply(lambda x: f"{x*100:.2f}%")
            
            render_data_table(summary_df_display)
            
            st.divider()
            
            # Performance ranking
            st.subheader("🏆 Performance Rankings")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Ranked by Sharpe Ratio (Risk-Adjusted Return)**")
                ranked_sharpe = summary_df.nlargest(5, 'sharpe_ratio')[['ticker', 'sharpe_ratio']]
                for idx, (i, row) in enumerate(ranked_sharpe.iterrows(), 1):
                    st.write(f"{idx}. {row['ticker']}: {row['sharpe_ratio']:.2f}")
            
            with col2:
                st.write("**Ranked by Annual Return**")
                ranked_return = summary_df.nlargest(5, 'annual_return')[['ticker', 'annual_return']]
                for idx, (i, row) in enumerate(ranked_return.iterrows(), 1):
                    st.write(f"{idx}. {row['ticker']}: {row['annual_return']*100:.1f}%")
            
            with col3:
                st.write("**Ranked by Volatility (Lowest = Most Stable)**")
                ranked_vol = summary_df.nsmallest(5, 'annual_volatility')[['ticker', 'annual_volatility']]
                for idx, (i, row) in enumerate(ranked_vol.iterrows(), 1):
                    st.write(f"{idx}. {row['ticker']}: {row['annual_volatility']*100:.1f}%")
    
    except Exception as e:
        st.error(f"Error generating summary: {e}")

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
render_footer()
