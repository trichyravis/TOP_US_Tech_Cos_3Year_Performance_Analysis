
"""
═══════════════════════════════════════════════════════════════════════════════
THE MOUNTAIN PATH - WORLD OF FINANCE
Top US Tech Companies - 3 Year Performance Analysis
Five-Lens Framework Financial Evaluation
═══════════════════════════════════════════════════════════════════════════════

Prof. V. Ravichandran
28+ Years Corporate Finance & Banking Experience
10+ Years Academic Excellence
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
import traceback

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="The Mountain Path - Top US Tech Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SIMPLE DATA FETCHING (No modules needed)
# ============================================================================

TICKERS = {
    'NVDA': 'NVIDIA',
    'MSFT': 'Microsoft',
    'AAPL': 'Apple',
    'GOOGL': 'Alphabet',
    'AMZN': 'Amazon'
}

@st.cache_data(ttl=3600)
def fetch_stock_data(ticker, period="3y"):
    """Fetch stock data from yfinance"""
    try:
        data = yf.download(ticker, period=period, progress=False)
        
        # Handle MultiIndex columns
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(1)
        
        # Standardize to lowercase
        data.columns = [col.lower() for col in data.columns]
        
        return data
    except:
        return None

@st.cache_data(ttl=3600)
def fetch_all_companies(period="3y"):
    """Fetch data for all 5 companies"""
    all_data = {}
    for ticker in TICKERS.keys():
        try:
            price_data = fetch_stock_data(ticker, period=period)
            stock = yf.Ticker(ticker)
            company_info = stock.info
            all_data[ticker] = {
                'price_data': price_data,
                'company_info': company_info
            }
        except:
            all_data[ticker] = {
                'price_data': None,
                'company_info': {}
            }
    return all_data

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

def calculate_volatility(returns):
    """Calculate annual volatility"""
    if returns is None or len(returns) < 2:
        return 0.0
    return returns.std() * np.sqrt(252)

def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    """Calculate Sharpe ratio"""
    if len(returns) < 2:
        return 0.0
    annual_return = returns.mean() * 252
    annual_volatility = returns.std() * np.sqrt(252)
    if annual_volatility == 0:
        return 0.0
    return (annual_return - risk_free_rate) / annual_volatility

def calculate_max_drawdown(prices):
    """Calculate maximum drawdown"""
    if prices is None or len(prices) < 2:
        return 0.0
    running_max = prices.expanding().max()
    drawdown = (prices - running_max) / running_max
    return drawdown.min()

# ============================================================================
# HEADER
# ============================================================================

st.markdown("---")
st.title("📊 THE MOUNTAIN PATH - WORLD OF FINANCE")
st.markdown("## Top US Tech Companies - 3 Year Performance Analysis")
st.markdown("---")

# ============================================================================
# TABS
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📖 About",
    "💰 Financial Performance",
    "📈 Market Analysis",
    "⚠️ Risk Analysis",
    "📋 Summary"
])

# ============================================================================
# TAB 1: ABOUT
# ============================================================================

with tab1:
    st.subheader("📖 About The Mountain Path - World of Finance")
    
    st.markdown("""
    ### Platform Overview
    
    Welcome to **The Mountain Path - World of Finance**, an educational platform designed to help MBA, CFA, and FRM students understand advanced financial analysis through practical application.
    
    ### 🎯 Our Mission
    
    To bridge the gap between theoretical finance concepts and real-world investment analysis using professional-grade frameworks and live market data.
    
    ### 📊 Analysis Framework
    
    This platform analyzes the top 5 US tech companies using a comprehensive **Five-Lens Financial Framework**:
    
    1. **Valuation Lens** - Is the company fairly priced?
    2. **Quality Lens** - How good is the business?
    3. **Growth Lens** - What's the growth trajectory?
    4. **Financial Health** - Is the balance sheet strong?
    5. **Risk & Momentum** - What's the risk profile?
    
    ### 🏢 Companies Analyzed
    
    - **NVDA** - NVIDIA
    - **MSFT** - Microsoft
    - **AAPL** - Apple
    - **GOOGL** - Alphabet
    - **AMZN** - Amazon
    
    ### 📚 Educational Resources
    
    This platform is built for students and professionals learning:
    - Fundamental analysis
    - Technical analysis
    - Risk management
    - Portfolio evaluation
    - Investment decision-making
    
    ### 🔗 Important Disclaimer
    
    **This tool is for educational purposes only. It is NOT investment advice.**
    
    Always consult with a qualified financial advisor before making investment decisions.
    
    ---
    
    *Built with ❤️ for financial education*
    """)

# ============================================================================
# TAB 2: FINANCIAL PERFORMANCE
# ============================================================================

with tab2:
    st.subheader("💰 Financial Performance - 5 US Tech Companies")
    
    st.markdown("### 📊 5-Company Analysis")
    
    try:
        all_data = fetch_all_companies(period="3y")
        
        if all_data:
            # Summary table
            summary_rows = []
            
            for ticker, data in all_data.items():
                company_name = TICKERS.get(ticker, ticker)
                company_info = data.get('company_info', {})
                price_data = data.get('price_data')
                
                if price_data is not None and not price_data.empty:
                    try:
                        if 'close' in price_data.columns:
                            close_prices = price_data['close']
                        else:
                            close_prices = price_data.iloc[:, -1]
                        
                        annual_return = calculate_annual_return(close_prices) * 100
                        returns = calculate_returns(close_prices).dropna()
                        volatility = calculate_volatility(returns) * 100
                        sharpe = calculate_sharpe_ratio(returns)
                        
                        summary_rows.append({
                            'Company': ticker,
                            'Name': company_name,
                            'Annual Return (%)': f"{annual_return:.2f}",
                            'Volatility (%)': f"{volatility:.2f}",
                            'Sharpe Ratio': f"{sharpe:.2f}"
                        })
                    except:
                        pass
            
            if summary_rows:
                summary_df = pd.DataFrame(summary_rows)
                st.dataframe(summary_df, use_container_width=True)
            
            st.divider()
            
            # Detailed company cards
            st.markdown("### 📋 Company Details")
            
            for ticker, data in all_data.items():
                company_name = TICKERS.get(ticker, ticker)
                company_info = data.get('company_info', {})
                
                with st.expander(f"📈 {ticker} - {company_name}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        pe = company_info.get('trailingPE', 'N/A')
                        st.metric("P/E Ratio", pe)
                        
                        pb = company_info.get('priceToBook', 'N/A')
                        st.metric("P/B Ratio", pb)
                    
                    with col2:
                        roe = company_info.get('returnOnEquity')
                        if roe:
                            st.metric("ROE", f"{roe*100:.1f}%")
                        else:
                            st.metric("ROE", "N/A")
                        
                        dividend = company_info.get('dividendYield')
                        if dividend:
                            st.metric("Dividend Yield", f"{dividend*100:.2f}%")
                        else:
                            st.metric("Dividend Yield", "N/A")
                    
                    with col3:
                        sector = company_info.get('sector', 'Technology')
                        st.metric("Sector", sector)
                        
                        market_cap = company_info.get('marketCap')
                        if market_cap:
                            st.metric("Market Cap", f"${market_cap/1e12:.2f}T")
                        else:
                            st.metric("Market Cap", "N/A")
    
    except Exception as e:
        st.error(f"❌ Error loading financial data: {str(e)}")

# ============================================================================
# TAB 3: MARKET ANALYSIS
# ============================================================================

with tab3:
    st.subheader("📈 Market Analysis")
    
    st.markdown("### 📉 Price Charts (3-Year History)")
    
    try:
        all_data = fetch_all_companies(period="3y")
        
        if all_data:
            # Create tabs for each company
            chart_tabs = st.tabs([f"{ticker} - {TICKERS[ticker]}" for ticker in TICKERS.keys()])
            
            for idx, ticker in enumerate(TICKERS.keys()):
                with chart_tabs[idx]:
                    data = all_data[ticker]
                    price_data = data.get('price_data')
                    company_name = TICKERS[ticker]
                    
                    if price_data is not None and not price_data.empty:
                        try:
                            # Get OHLC columns
                            if all(col in price_data.columns for col in ['open', 'high', 'low', 'close']):
                                fig = go.Figure(data=[go.Candlestick(
                                    x=price_data.index,
                                    open=price_data['open'],
                                    high=price_data['high'],
                                    low=price_data['low'],
                                    close=price_data['close']
                                )])
                                
                                fig.update_layout(
                                    title=f"{ticker} - {company_name} (3-Year)",
                                    yaxis_title="Price ($)",
                                    xaxis_title="Date",
                                    template="plotly_white",
                                    height=500
                                )
                                
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.warning(f"⚠️ OHLC data not available for {ticker}")
                        except Exception as e:
                            st.error(f"❌ Error displaying chart for {ticker}")
                    else:
                        st.warning(f"❌ No price data for {ticker}")
    
    except Exception as e:
        st.error(f"❌ Error in market analysis: {str(e)}")

# ============================================================================
# TAB 4: RISK ANALYSIS
# ============================================================================

with tab4:
    st.subheader("⚠️ Risk Analysis")
    
    st.markdown("### 📊 Risk Metrics Comparison")
    
    try:
        all_data = fetch_all_companies(period="3y")
        
        if all_data:
            risk_data = []
            
            for ticker, data in all_data.items():
                price_data = data.get('price_data')
                company_name = TICKERS.get(ticker, ticker)
                
                if price_data is not None and not price_data.empty:
                    try:
                        if 'close' in price_data.columns:
                            close_prices = price_data['close']
                        else:
                            close_prices = price_data.iloc[:, -1]
                        
                        returns = calculate_returns(close_prices).dropna()
                        
                        if not returns.empty:
                            annual_return = calculate_annual_return(close_prices) * 100
                            volatility = calculate_volatility(returns) * 100
                            sharpe = calculate_sharpe_ratio(returns)
                            max_dd = calculate_max_drawdown(close_prices) * 100
                            
                            risk_data.append({
                                'Company': ticker,
                                'Return (%)': f"{annual_return:.2f}",
                                'Volatility (%)': f"{volatility:.2f}",
                                'Sharpe Ratio': f"{sharpe:.2f}",
                                'Max Drawdown (%)': f"{max_dd:.2f}"
                            })
                    except:
                        pass
            
            if risk_data:
                risk_df = pd.DataFrame(risk_data)
                st.dataframe(risk_df, use_container_width=True)
                
                st.divider()
                
                # Volatility chart
                volatility_data = {}
                for row in risk_data:
                    ticker = row['Company']
                    volatility_data[ticker] = float(row['Volatility (%)'])
                
                fig = go.Figure(data=[go.Bar(
                    x=list(volatility_data.keys()),
                    y=list(volatility_data.values()),
                    marker_color=['#FF6B6B' if v > 25 else '#4ECDC4' for v in volatility_data.values()]
                )])
                
                fig.update_layout(
                    title="Annual Volatility Comparison",
                    xaxis_title="Company",
                    yaxis_title="Volatility (%)",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"❌ Error in risk analysis: {str(e)}")

# ============================================================================
# TAB 5: SUMMARY
# ============================================================================

with tab5:
    st.subheader("📋 Summary & Key Insights")
    
    st.markdown("""
    ### 📊 Analysis Overview
    
    This platform provides comprehensive analysis of the top 5 US technology companies
    based on 3 years of historical market data.
    
    ### 🎯 Key Takeaways
    
    1. **Valuation** - See how companies compare on price metrics
    2. **Growth** - Understand revenue and earnings trends
    3. **Quality** - Evaluate profitability and efficiency
    4. **Financial Health** - Assess balance sheet strength
    5. **Risk** - Measure volatility and downside risk
    
    ### ⚠️ Important Notes
    
    - **Educational Use Only** - Not investment advice
    - **Consult Professionals** - Always speak with a financial advisor
    - **Past Performance** - Does not guarantee future results
    - **Data Sources** - Yahoo Finance and public company filings
    
    ### 📞 More Information
    
    For questions about financial analysis, investing, or this platform,
    please consult with a qualified financial advisor or educator.
    
    ---
    
    **Prof. V. Ravichandran**
    
    28+ Years Corporate Finance & Banking Experience
    
    10+ Years Academic Excellence
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

🔗 [LinkedIn](https://linkedin.com/in/trichyravis) | 🐙 [GitHub](https://github.com)

**Disclaimer:** This tool is for educational purposes. Not financial advice. Always consult with a qualified financial advisor before making investment decisions.

© 2026 The Mountain Path - World of Finance

📊 Last Updated: 2026-01-11 | Data: Yahoo Finance

</div>
""", unsafe_allow_html=True)
