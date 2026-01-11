
"""
THE MOUNTAIN PATH - WORLD OF FINANCE
Top US Tech Companies - 3 Year Performance Analysis
Prof. V. Ravichandran | 28+ Years Finance Experience
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="The Mountain Path",
    page_icon="📊",
    layout="wide"
)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### ⚙️ Controls")
    st.markdown("---")
    
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.info("📊 Analyzing 3 Years of data")

# ============================================================================
# TICKERS
# ============================================================================

TICKERS = {
    'NVDA': 'NVIDIA',
    'MSFT': 'Microsoft',
    'AAPL': 'Apple',
    'GOOGL': 'Alphabet',
    'AMZN': 'Amazon'
}

# ============================================================================
# HEADER
# ============================================================================

st.title("📊 THE MOUNTAIN PATH - WORLD OF FINANCE")
st.markdown("## Top US Tech Companies - 3 Year Performance Analysis")
st.markdown("---")

# ============================================================================
# FETCH DATA
# ============================================================================

def get_data(ticker):
    """Get stock data from yfinance"""
    try:
        data = yf.download(ticker, period="3y", progress=False)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(1)
        data.columns = [col.lower() for col in data.columns]
        return data
    except:
        return None

# ============================================================================
# TABS
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📖 About",
    "💰 Financial",
    "📈 Market",
    "⚠️ Risk",
    "📋 Summary"
])

# ============================================================================
# TAB 1: ABOUT
# ============================================================================

with tab1:
    st.subheader("📖 About This Platform")
    st.markdown("""
    ### Welcome to The Mountain Path
    
    This educational platform analyzes the top 5 US technology companies
    using professional financial frameworks.
    
    ### Companies Analyzed
    - NVDA (NVIDIA)
    - MSFT (Microsoft)
    - AAPL (Apple)
    - GOOGL (Alphabet)
    - AMZN (Amazon)
    
    ### Data Period
    - 3 years of historical data
    - Updated from Yahoo Finance
    
    ### Disclaimer
    **Educational purposes only. Not investment advice.**
    """)

# ============================================================================
# TAB 2: FINANCIAL PERFORMANCE
# ============================================================================

with tab2:
    st.subheader("💰 Financial Performance")
    
    st.markdown("### Company Analysis")
    
    metrics = []
    
    for ticker in TICKERS.keys():
        data = get_data(ticker)
        
        if data is not None and not data.empty:
            try:
                if 'close' in data.columns:
                    close = data['close']
                else:
                    close = data.iloc[:, -1]
                
                # Calculate metrics
                start_price = close.iloc[0]
                end_price = close.iloc[-1]
                return_3y = ((end_price - start_price) / start_price) * 100
                
                returns = close.pct_change().dropna()
                volatility = returns.std() * np.sqrt(252) * 100
                
                metrics.append({
                    'Company': ticker,
                    'Name': TICKERS[ticker],
                    '3Y Return (%)': f"{return_3y:.2f}",
                    'Volatility (%)': f"{volatility:.2f}"
                })
            except:
                pass
    
    if metrics:
        df = pd.DataFrame(metrics)
        st.dataframe(df, use_container_width=True)

# ============================================================================
# TAB 3: MARKET ANALYSIS
# ============================================================================

with tab3:
    st.subheader("📈 Market Analysis")
    
    st.markdown("### Price Charts (3-Year)")
    
    # Create tabs for each company
    chart_tabs = st.tabs([f"{t} - {TICKERS[t]}" for t in TICKERS.keys()])
    
    for idx, ticker in enumerate(TICKERS.keys()):
        with chart_tabs[idx]:
            data = get_data(ticker)
            
            if data is not None and not data.empty:
                try:
                    # Check for OHLC data
                    has_ohlc = all(col in data.columns for col in ['open', 'high', 'low', 'close'])
                    
                    if has_ohlc:
                        # Candlestick chart
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
                        
                        # Show close price chart instead
                        if 'close' in data.columns:
                            fig = go.Figure()
                            fig.add_trace(go.Scatter(
                                x=data.index,
                                y=data['close'],
                                mode='lines',
                                name='Close Price'
                            ))
                            fig.update_layout(
                                title=f"{ticker} - {TICKERS[ticker]} (Close Price)",
                                yaxis_title="Price ($)",
                                height=500,
                                template="plotly_white"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error displaying chart for {ticker}: {str(e)}")
            else:
                st.warning(f"No data available for {ticker}")

# ============================================================================
# TAB 4: RISK ANALYSIS
# ============================================================================

with tab4:
    st.subheader("⚠️ Risk Analysis")
    
    st.markdown("### Risk Metrics")
    
    risk_metrics = []
    
    for ticker in TICKERS.keys():
        data = get_data(ticker)
        
        if data is not None and not data.empty:
            try:
                if 'close' in data.columns:
                    close = data['close']
                else:
                    close = data.iloc[:, -1]
                
                returns = close.pct_change().dropna()
                
                # Calculate risk metrics
                annual_vol = returns.std() * np.sqrt(252) * 100
                annual_return = (close.iloc[-1] / close.iloc[0] - 1) * 100 / 3
                sharpe = (annual_return / annual_vol) if annual_vol > 0 else 0
                
                # Max drawdown
                running_max = close.expanding().max()
                drawdown = (close - running_max) / running_max
                max_dd = drawdown.min() * 100
                
                risk_metrics.append({
                    'Company': ticker,
                    'Volatility (%)': f"{annual_vol:.2f}",
                    'Annual Return (%)': f"{annual_return:.2f}",
                    'Sharpe Ratio': f"{sharpe:.2f}",
                    'Max Drawdown (%)': f"{max_dd:.2f}"
                })
            except:
                pass
    
    if risk_metrics:
        df = pd.DataFrame(risk_metrics)
        st.dataframe(df, use_container_width=True)
        
        st.divider()
        
        # Volatility chart
        st.markdown("### Volatility Comparison")
        
        vol_data = {row['Company']: float(row['Volatility (%)']) for row in risk_metrics}
        
        fig = go.Figure(data=[go.Bar(
            x=list(vol_data.keys()),
            y=list(vol_data.values()),
            marker_color='#1f77b4'
        )])
        
        fig.update_layout(
            title="Annual Volatility",
            xaxis_title="Company",
            yaxis_title="Volatility (%)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 5: SUMMARY
# ============================================================================

with tab5:
    st.subheader("📋 Summary")
    
    st.markdown("""
    ### Analysis Overview
    
    This platform provides comprehensive analysis of top US tech companies
    using 3 years of historical data from Yahoo Finance.
    
    ### Key Features
    
    1. **Financial Performance** - Returns and volatility metrics
    2. **Market Analysis** - Candlestick charts and price trends
    3. **Risk Analysis** - Volatility, Sharpe ratio, and drawdowns
    
    ### Important Disclaimer
    
    ⚠️ **This is for educational purposes only**
    
    This is NOT investment advice. Always consult with a qualified
    financial advisor before making investment decisions.
    
    ### Data Source
    
    All data is sourced from Yahoo Finance (yfinance) and represents
    publicly available market information.
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center'>

### 🏔️ THE MOUNTAIN PATH - WORLD OF FINANCE

**Top US Tech Companies 3 Year Performance Analysis**

Prof. V. Ravichandran | 28+ Years Finance Experience

**Disclaimer:** Educational purposes only. Not financial advice.

© 2026 The Mountain Path - World of Finance

</div>
""", unsafe_allow_html=True)
