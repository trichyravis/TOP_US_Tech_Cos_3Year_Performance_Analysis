
"""
THE MOUNTAIN PATH - WORLD OF FINANCE
Top US Tech Companies - 3 Year Performance Analysis
Prof. V. Ravichandran | 28+ Years Finance Experience
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="The Mountain Path - Finance",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CONSTANTS
# ============================================================================

TICKERS = {
    'NVDA': 'NVIDIA',
    'MSFT': 'Microsoft',
    'AAPL': 'Apple',
    'GOOGL': 'Alphabet',
    'AMZN': 'Amazon'
}

COLORS = {
    'primary': '#003366',
    'secondary': '#0088CC',
    'error': '#DC3545'
}

DISCLAIMER = """
⚠️ **DISCLAIMER**: This tool is for **EDUCATIONAL PURPOSES ONLY**. 
This is NOT investment advice. Always consult with a qualified financial advisor 
before making investment decisions. Past performance does not guarantee future results.
"""

LINKEDIN_URL = "https://linkedin.com/in/trichyravis"
GITHUB_URL = "https://github.com/trichyravis"

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### ⚙️ Navigation")
    st.markdown("---")
    
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.info("📊 Analyzing 3 Years of data for 5 companies")
    
    st.markdown("---")
    st.markdown("### ⚙️ Risk Parameters")
    confidence = st.radio("VaR Confidence Level:", [90, 95, 99], index=1) / 100

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_data(ttl=3600)
def get_stock_data(ticker, period="3y"):
    """Fetch stock data from yfinance"""
    try:
        data = yf.download(ticker, period=period, progress=False)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(1)
        data.columns = [col.lower() for col in data.columns]
        return data
    except:
        return None

def calculate_returns(prices):
    """Calculate daily returns"""
    if prices is None or len(prices) < 2:
        return pd.Series()
    return prices.pct_change()

def calculate_annual_return(prices):
    """Calculate annualized return"""
    if prices is None or len(prices) < 2:
        return 0.0
    start = prices.iloc[0]
    end = prices.iloc[-1]
    years = len(prices) / 252
    return (end / start) ** (1 / years) - 1 if years > 0 else 0.0

def calculate_volatility(returns, annualize=True):
    """Calculate volatility"""
    if returns is None or len(returns) < 2:
        return 0.0
    vol = returns.std()
    return vol * np.sqrt(252) if annualize else vol

def calculate_sharpe_ratio(returns, rf_rate=0.02):
    """Calculate Sharpe ratio"""
    if len(returns) < 2:
        return 0.0
    annual_return = returns.mean() * 252
    annual_vol = returns.std() * np.sqrt(252)
    if annual_vol == 0:
        return 0.0
    return (annual_return - rf_rate) / annual_vol

def calculate_sortino_ratio(returns, rf_rate=0.02):
    """Calculate Sortino ratio"""
    if len(returns) < 2:
        return 0.0
    annual_return = returns.mean() * 252
    downside = returns[returns < 0].std() * np.sqrt(252)
    if downside == 0:
        return 0.0
    return (annual_return - rf_rate) / downside

def calculate_var_cvar(returns, confidence=0.95):
    """Calculate VaR and CVaR"""
    var = returns.quantile(1 - confidence)
    cvar = returns[returns <= var].mean()
    return var, cvar

def calculate_max_drawdown(prices):
    """Calculate maximum drawdown"""
    if prices is None or len(prices) < 2:
        return 0.0
    running_max = prices.expanding().max()
    drawdown = (prices - running_max) / running_max
    return drawdown.min()

def generate_risk_summary(ticker, prices, returns, rf_rate=0.02):
    """Generate risk summary for a stock"""
    annual_return = calculate_annual_return(prices)
    annual_vol = calculate_volatility(returns)
    sharpe = calculate_sharpe_ratio(returns, rf_rate)
    sortino = calculate_sortino_ratio(returns, rf_rate)
    var_95, cvar_95 = calculate_var_cvar(returns, 0.95)
    max_dd = calculate_max_drawdown(prices)
    
    return {
        'ticker': ticker,
        'annual_return': annual_return,
        'annual_volatility': annual_vol,
        'sharpe_ratio': sharpe,
        'sortino_ratio': sortino,
        'var_95': var_95,
        'cvar_95': cvar_95,
        'max_drawdown': max_dd
    }

# ============================================================================
# HEADER
# ============================================================================

st.title("📊 THE MOUNTAIN PATH - WORLD OF FINANCE")
st.markdown("## Top US Tech Companies - 3 Year Performance Analysis")
st.markdown("---")

# ============================================================================
# TABS
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 About",
    "💰 Financial",
    "📈 Market",
    "⚠️ Risk",
    "📊 Summary"
])

# ============================================================================
# TAB 1: ABOUT
# ============================================================================

with tab1:
    st.subheader("About The Mountain Path - World of Finance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📚 Platform Overview
        
        **The Mountain Path** is an educational platform for financial analysis.
        
        ### 🎯 Companies Analyzed
        - **NVIDIA** (NVDA) - AI & Semiconductors
        - **Microsoft** (MSFT) - Cloud & Software
        - **Apple** (AAPL) - Consumer Electronics
        - **Alphabet** (GOOGL) - Digital Advertising
        - **Amazon** (AMZN) - E-commerce & Cloud
        
        ### 📊 Analysis Features
        ✓ 3-year historical data  
        ✓ Financial metrics  
        ✓ Risk analysis (Sharpe, Sortino, VaR)  
        ✓ Interactive charts  
        ✓ Real-time data  
        """)
    
    with col2:
        st.markdown("""
        ### 🔧 Key Metrics
        
        - Annual Return
        - Volatility
        - Sharpe Ratio
        - Sortino Ratio
        - Value-at-Risk (VaR)
        - Max Drawdown
        - Revenue & Income
        - Market Cap
        
        ### 📞 Contact
        
        **Prof. V. Ravichandran**
        
        28+ Years Finance & Banking
        
        10+ Years Academic Excellence
        """)
    
    st.divider()
    st.warning(DISCLAIMER)

# ============================================================================
# TAB 2: FINANCIAL PERFORMANCE
# ============================================================================

with tab2:
    st.subheader("💰 Financial Performance")
    st.info("📊 Analyzing all 5 companies: NVDA, MSFT, AAPL, GOOGL, AMZN")
    
    try:
        financial_data = []
        
        for ticker in TICKERS.keys():
            try:
                ticker_obj = yf.Ticker(ticker)
                info = ticker_obj.info
                
                financial_data.append({
                    'Company': f"{ticker} - {TICKERS[ticker]}",
                    'Revenue ($B)': round(info.get('totalRevenue', 0) / 1e9, 2),
                    'Operating Income ($B)': round(info.get('operatingIncome', 0) / 1e9, 2),
                    'Net Income ($B)': round(info.get('netIncome', 0) / 1e9, 2),
                    'Market Cap ($B)': round(info.get('marketCap', 0) / 1e9, 2),
                })
            except:
                pass
        
        if financial_data:
            df = pd.DataFrame(financial_data)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Highest Revenue", f"${df['Revenue ($B)'].max():.1f}B")
            with col2:
                st.metric("Highest Net Income", f"${df['Net Income ($B)'].max():.1f}B")
            with col3:
                st.metric("Largest Market Cap", f"${df['Market Cap ($B)'].max():.1f}B")
            
            st.subheader("Financial Metrics Comparison")
            st.dataframe(df, use_container_width=True)
            
            st.subheader("Individual Company Details")
            
            for ticker in TICKERS.keys():
                with st.expander(f"📈 {ticker} - {TICKERS[ticker]}"):
                    company_data = df[df['Company'].str.contains(ticker)]
                    if not company_data.empty:
                        company_data = company_data.iloc[0]
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Revenue", f"${company_data['Revenue ($B)']:.1f}B")
                        with col2:
                            st.metric("Op Income", f"${company_data['Operating Income ($B)']:.1f}B")
                        with col3:
                            st.metric("Net Income", f"${company_data['Net Income ($B)']:.1f}B")
                        with col4:
                            st.metric("Market Cap", f"${company_data['Market Cap ($B)']:.1f}B")
    
    except Exception as e:
        st.error(f"Error: {e}")

# ============================================================================
# TAB 3: MARKET ANALYSIS
# ============================================================================

with tab3:
    st.subheader("📈 Market Analysis")
    st.info("📊 Analyzing all 5 companies: NVDA, MSFT, AAPL, GOOGL, AMZN")
    
    try:
        price_data_dict = {}
        for ticker in TICKERS.keys():
            data = get_stock_data(ticker)
            if data is not None:
                price_data_dict[ticker] = data
        
        if price_data_dict:
            # Candlestick charts
            st.subheader("📉 Price Charts (3-Year)")
            
            chart_tabs = st.tabs([f"{t} - {TICKERS[t]}" for t in TICKERS.keys()])
            
            for idx, ticker in enumerate(TICKERS.keys()):
                with chart_tabs[idx]:
                    if ticker in price_data_dict:
                        data = price_data_dict[ticker]
                        
                        has_ohlc = all(col in data.columns for col in ['open', 'high', 'low', 'close'])
                        
                        if has_ohlc:
                            fig = go.Figure(data=[go.Candlestick(
                                x=data.index,
                                open=data['open'],
                                high=data['high'],
                                low=data['low'],
                                close=data['close']
                            )])
                            
                            fig.update_layout(
                                title=f"{ticker} - {TICKERS[ticker]}",
                                yaxis_title="Price ($)",
                                height=500,
                                template="plotly_white"
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning(f"OHLC data not available for {ticker}")
            
            # Returns comparison
            st.subheader("📊 Annual Returns Comparison")
            
            annual_returns = {}
            for ticker, data in price_data_dict.items():
                close_col = 'close' if 'close' in data.columns else 'Close'
                annual_return = calculate_annual_return(data[close_col])
                annual_returns[ticker] = annual_return * 100
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=list(annual_returns.keys()),
                y=list(annual_returns.values()),
                marker_color=[COLORS['primary'] if v > 0 else '#d62728' for v in annual_returns.values()]
            ))
            
            fig.update_layout(
                title="3-Year Annualized Returns",
                xaxis_title="Company",
                yaxis_title="Annual Return (%)",
                height=400,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Volatility
            st.subheader("Volatility Comparison")
            
            volatilities = {}
            for ticker, data in price_data_dict.items():
                returns = calculate_returns(data['close'] if 'close' in data.columns else data['Close'])
                vol = calculate_volatility(returns)
                volatilities[ticker] = vol * 100
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=list(volatilities.keys()),
                y=list(volatilities.values()),
                marker_color=COLORS['secondary']
            ))
            
            fig.update_layout(
                title="Annual Volatility",
                xaxis_title="Company",
                yaxis_title="Volatility (%)",
                height=400,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error: {e}")

# ============================================================================
# TAB 4: RISK ANALYSIS
# ============================================================================

with tab4:
    st.subheader("⚠️ Risk Analysis")
    st.info(f"📊 Risk metrics at {int(confidence*100)}% confidence level")
    
    try:
        risk_summaries = []
        
        for ticker in TICKERS.keys():
            data = get_stock_data(ticker)
            if data is not None:
                close_col = 'close' if 'close' in data.columns else 'Close'
                returns = calculate_returns(data[close_col])
                summary = generate_risk_summary(ticker, data[close_col], returns)
                risk_summaries.append(summary)
        
        if risk_summaries:
            risk_df = pd.DataFrame(risk_summaries)
            
            # Key metrics
            st.subheader("🎯 Key Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                best_sharpe_ticker = risk_df.loc[risk_df['sharpe_ratio'].idxmax(), 'ticker']
                best_sharpe = risk_df['sharpe_ratio'].max()
                st.metric("Best Sharpe Ratio", best_sharpe_ticker, f"{best_sharpe:.2f}")
            
            with col2:
                best_sortino_ticker = risk_df.loc[risk_df['sortino_ratio'].idxmax(), 'ticker']
                best_sortino = risk_df['sortino_ratio'].max()
                st.metric("Best Sortino Ratio", best_sortino_ticker, f"{best_sortino:.2f}")
            
            with col3:
                lowest_vol_ticker = risk_df.loc[risk_df['annual_volatility'].idxmin(), 'ticker']
                lowest_vol = risk_df['annual_volatility'].min()
                st.metric("Lowest Volatility", lowest_vol_ticker, f"{lowest_vol*100:.1f}%")
            
            with col4:
                max_return_ticker = risk_df.loc[risk_df['annual_return'].idxmax(), 'ticker']
                max_return = risk_df['annual_return'].max()
                st.metric("Best Return", max_return_ticker, f"{max_return*100:.1f}%")
            
            st.divider()
            
            # Risk metrics table
            st.subheader("Risk Metrics Dashboard")
            
            display_df = risk_df.copy()
            display_df['annual_return'] = display_df['annual_return'].apply(lambda x: f"{x*100:.2f}%")
            display_df['annual_volatility'] = display_df['annual_volatility'].apply(lambda x: f"{x*100:.2f}%")
            display_df['sharpe_ratio'] = display_df['sharpe_ratio'].apply(lambda x: f"{x:.2f}")
            display_df['sortino_ratio'] = display_df['sortino_ratio'].apply(lambda x: f"{x:.2f}")
            display_df['var_95'] = display_df['var_95'].apply(lambda x: f"{x*100:.2f}%")
            display_df['max_drawdown'] = display_df['max_drawdown'].apply(lambda x: f"{x*100:.2f}%")
            
            st.dataframe(display_df[['ticker', 'annual_return', 'annual_volatility', 'sharpe_ratio', 'sortino_ratio', 'max_drawdown']], use_container_width=True)
    
    except Exception as e:
        st.error(f"Error: {e}")

# ============================================================================
# TAB 5: SUMMARY
# ============================================================================

with tab5:
    st.subheader("📊 Executive Summary")
    
    try:
        all_summaries = []
        
        for ticker in TICKERS.keys():
            data = get_stock_data(ticker)
            if data is not None:
                close_col = 'close' if 'close' in data.columns else 'Close'
                returns = calculate_returns(data[close_col])
                summary = generate_risk_summary(ticker, data[close_col], returns)
                all_summaries.append(summary)
        
        if all_summaries:
            summary_df = pd.DataFrame(all_summaries)
            
            # Key insights
            st.subheader("🎯 Key Insights")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                best_return = summary_df['annual_return'].max()
                best_return_ticker = summary_df.loc[summary_df['annual_return'].idxmax(), 'ticker']
                st.metric("Best Performer", best_return_ticker, f"{best_return*100:.1f}%")
            
            with col2:
                best_sharpe = summary_df['sharpe_ratio'].max()
                best_sharpe_ticker = summary_df.loc[summary_df['sharpe_ratio'].idxmax(), 'ticker']
                st.metric("Best Risk-Adjusted", best_sharpe_ticker, f"{best_sharpe:.2f}")
            
            with col3:
                lowest_vol = summary_df['annual_volatility'].min()
                lowest_vol_ticker = summary_df.loc[summary_df['annual_volatility'].idxmin(), 'ticker']
                st.metric("Most Stable", lowest_vol_ticker, f"{lowest_vol*100:.1f}%")
            
            st.divider()
            
            # Comparison table
            st.subheader("📋 Complete Metrics")
            
            display_df = summary_df.copy()
            display_df['annual_return'] = display_df['annual_return'].apply(lambda x: f"{x*100:.2f}%")
            display_df['annual_volatility'] = display_df['annual_volatility'].apply(lambda x: f"{x*100:.2f}%")
            display_df['sharpe_ratio'] = display_df['sharpe_ratio'].apply(lambda x: f"{x:.2f}")
            display_df['sortino_ratio'] = display_df['sortino_ratio'].apply(lambda x: f"{x:.2f}")
            display_df['max_drawdown'] = display_df['max_drawdown'].apply(lambda x: f"{x*100:.2f}%")
            
            st.dataframe(display_df, use_container_width=True)
            
            st.divider()
            
            # Rankings
            st.subheader("🏆 Performance Rankings")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Sharpe Ratio (Risk-Adjusted)**")
                ranked = summary_df.nlargest(5, 'sharpe_ratio')[['ticker', 'sharpe_ratio']]
                for idx, (i, row) in enumerate(ranked.iterrows(), 1):
                    st.write(f"{idx}. {row['ticker']}: {row['sharpe_ratio']:.2f}")
            
            with col2:
                st.write("**Annual Return**")
                ranked = summary_df.nlargest(5, 'annual_return')[['ticker', 'annual_return']]
                for idx, (i, row) in enumerate(ranked.iterrows(), 1):
                    st.write(f"{idx}. {row['ticker']}: {row['annual_return']*100:.1f}%")
            
            with col3:
                st.write("**Lowest Volatility**")
                ranked = summary_df.nsmallest(5, 'annual_volatility')[['ticker', 'annual_volatility']]
                for idx, (i, row) in enumerate(ranked.iterrows(), 1):
                    st.write(f"{idx}. {row['ticker']}: {row['annual_volatility']*100:.1f}%")
    
    except Exception as e:
        st.error(f"Error: {e}")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center'>

### 🏔️ THE MOUNTAIN PATH - WORLD OF FINANCE

**Top US Tech Companies 3 Year Performance Analysis**

Prof. V. Ravichandran | 28+ Years Finance Experience | 10+ Years Academic Excellence

[LinkedIn](https://linkedin.com/in/trichyravis) | [GitHub](https://github.com)

**Disclaimer:** Educational purposes only. Not investment advice.

© 2026 The Mountain Path - World of Finance

</div>
""", unsafe_allow_html=True)
