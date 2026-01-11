
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
# IMPORTS
# ============================================================================

try:
    from financial_performance import FiveLensFramework
    from data_handler import DataFetcher, fetch_all_company_data, fetch_market_data
    FRAMEWORK_AVAILABLE = True
except:
    FRAMEWORK_AVAILABLE = False

# ============================================================================
# DATA
# ============================================================================

TICKERS = {
    'NVDA': 'NVIDIA',
    'MSFT': 'Microsoft',
    'AAPL': 'Apple',
    'GOOGL': 'Alphabet',
    'AMZN': 'Amazon'
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_data(ttl=3600)
def get_stock_data(ticker, period="3y"):
    """Fetch stock data from yfinance"""
    try:
        data = yf.download(ticker, period=period, progress=False)
        return data
    except:
        return None

# ============================================================================
# SIDEBAR
# ============================================================================

st.sidebar.markdown("### ⚙️ Settings")
st.sidebar.markdown("---")

time_period = st.sidebar.radio(
    "📊 Select Data Period",
    ("1 Year", "2 Years", "3 Years"),
    index=2
)

period_map = {"1 Year": "1y", "2 Years": "2y", "3 Years": "3y"}
selected_period = period_map[time_period]

st.sidebar.info(f"📊 Analyzing {time_period} of data")

# ============================================================================
# MAIN CONTENT
# ============================================================================

st.title("📊 THE MOUNTAIN PATH - WORLD OF FINANCE")
st.markdown("## Top US Tech Companies - 3 Year Performance Analysis")
st.markdown("---")

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📖 About",
    "💰 Financial Performance",
    "📈 Market Analysis",
    "⚠️  Risk Analysis",
    "📋 Summary"
])

# ============================================================================
# TAB 1: ABOUT
# ============================================================================

with tab1:
    st.markdown("""
    ### 🎯 Platform Overview
    
    **The Mountain Path - World of Finance** is an educational platform providing
    comprehensive financial analysis of top US technology companies.
    
    #### 📊 Technology Sector Analysis
    
    This platform analyzes the following companies:
    - **NVDA** - NVIDIA: Leading AI and GPU semiconductor company
    - **MSFT** - Microsoft: Cloud computing and enterprise software leader
    - **AAPL** - Apple: Consumer electronics and ecosystem innovator
    - **GOOGL** - Alphabet: Search, advertising, and cloud services
    - **AMZN** - Amazon: E-commerce and cloud infrastructure provider
    
    #### 🔍 Analysis Framework
    
    We use a comprehensive **Five-Lens Financial Analysis Framework**:
    
    1. **Valuation Lens (20%)** - P/E, P/B, P/S ratios and dividend yield
    2. **Quality Lens (25%)** - ROE, profit margins, ROIC, and asset returns
    3. **Growth Lens (20%)** - Revenue and earnings growth rates
    4. **Financial Health (20%)** - Leverage, liquidity, and cash flow metrics
    5. **Risk & Momentum (15%)** - Volatility, beta, Sharpe ratio, and price momentum
    
    Each metric is scored 0-100, and companies receive investment signals:
    - 🚀 **Strong Buy** (85+)
    - ✅ **Buy** (75-84)
    - 🟡 **Hold** (65-74)
    - ⚠️ **Watch** (50-64)
    - 🔴 **Avoid** (<50)
    
    #### 📊 Data Sources
    
    - **Price Data**: Yahoo Finance (3-year daily OHLCV)
    - **Financial Metrics**: Yahoo Finance and company filings
    - **Market Data**: S&P 500 index for comparison
    
    #### ⚠️ Important Disclaimer
    
    This analysis is **for educational purposes only** and should not be considered
    investment advice. Past performance does not guarantee future results. Always
    conduct your own research and consult a qualified financial advisor before
    making investment decisions.
    
    ---
    
    **Prof. V. Ravichandran**
    - 28+ Years Corporate Finance & Banking Experience
    - 10+ Years Academic Excellence
    """)

# ============================================================================
# TAB 2: FINANCIAL PERFORMANCE
# ============================================================================

with tab2:
    st.subheader("💰 Financial Performance Analysis")
    
    st.info("📊 Analyzing all 5 companies using Five-Lens Framework...")
    
    if not FRAMEWORK_AVAILABLE:
        st.error("❌ Five-Lens Framework not available. Please check dependencies.")
    else:
        try:
            # Fetch all company data
            all_data = fetch_all_company_data(period=selected_period)
            
            if not all_data:
                st.error("❌ Could not fetch financial data")
            else:
                framework = FiveLensFramework()
                analysis_results = []
                detailed_scores = {}
                
                # Analyze each company
                for ticker, data in all_data.items():
                    try:
                        company_info = data.get('company_info', {})
                        price_data = data.get('price_data')
                        
                        # Get company name from TICKERS mapping or yfinance
                        company_name = TICKERS.get(ticker, company_info.get('longName', company_info.get('shortName', 'Unknown')))
                        
                        # Initialize metrics with defaults
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
                        
                        # Try to get actual values from yfinance
                        if 'trailingPE' in company_info:
                            stock_data_eval['pe_ratio'] = company_info['trailingPE']
                        if 'priceToBook' in company_info:
                            stock_data_eval['pb_ratio'] = company_info['priceToBook']
                        if 'returnOnEquity' in company_info:
                            financial_metrics_eval['roe'] = company_info['returnOnEquity']
                        if 'profitMargins' in company_info:
                            financial_metrics_eval['npm'] = company_info['profitMargins']
                        
                        # Calculate risk metrics from price data
                        risk_metrics_eval = {
                            'beta': 1.2,
                            'volatility_252d': 0.25,
                            'sharpe_ratio': 0.8,
                        }
                        
                        if price_data is not None and not price_data.empty:
                            try:
                                # Handle MultiIndex columns
                                if isinstance(price_data.columns, pd.MultiIndex):
                                    price_data.columns = price_data.columns.get_level_values(1)
                                
                                price_data.columns = price_data.columns.str.lower()
                                
                                if 'close' in price_data.columns:
                                    close_prices = price_data['close']
                                else:
                                    close_prices = price_data.iloc[:, -1]
                                
                                returns = DataFetcher.calculate_returns(close_prices).dropna()
                                if not returns.empty:
                                    risk_metrics_eval['volatility_252d'] = DataFetcher.calculate_volatility(returns)
                                    risk_metrics_eval['sharpe_ratio'] = DataFetcher.calculate_sharpe_ratio(returns)
                            except:
                                pass
                        
                        # Evaluate using Five-Lens Framework
                        lens_scores = framework.evaluate_stock(stock_data_eval, financial_metrics_eval, risk_metrics_eval)
                        
                        analysis_results.append({
                            'Company': ticker,
                            'Name': company_name,
                            'Composite Score': f"{lens_scores.composite:.1f}",
                            'Valuation': f"{lens_scores.valuation:.1f}",
                            'Quality': f"{lens_scores.quality:.1f}",
                            'Growth': f"{lens_scores.growth:.1f}",
                            'Health': f"{lens_scores.financial_health:.1f}",
                            'Risk': f"{lens_scores.risk_momentum:.1f}",
                        })
                        
                        detailed_scores[ticker] = {
                            'scores': lens_scores,
                            'company_info': company_info,
                            'stock_data': stock_data_eval
                        }
                    except Exception as e:
                        st.warning(f"⚠️ Error analyzing {ticker}: {str(e)}")
                
                # Display results
                if analysis_results:
                    st.markdown("### 🎯 Five-Lens Analysis Summary")
                    results_df = pd.DataFrame(analysis_results)
                    st.dataframe(results_df, use_container_width=True)
                    
                    st.markdown("### 📊 Detailed Company Analysis")
                    
                    for ticker, data_dict in detailed_scores.items():
                        scores = data_dict['scores']
                        company_info = data_dict['company_info']
                        
                        company_name = company_info.get('longName', company_info.get('shortName', 'Unknown'))
                        signal, _ = framework.get_signal(scores.composite)
                        
                        with st.expander(f"📈 {ticker} - {company_name} | {signal}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.metric("Composite Score", f"{scores.composite:.1f}/100")
                                st.metric("Valuation Lens", f"{scores.valuation:.1f}")
                                st.metric("Quality Lens", f"{scores.quality:.1f}")
                                st.metric("Growth Lens", f"{scores.growth:.1f}")
                            
                            with col2:
                                st.metric("Financial Health", f"{scores.financial_health:.1f}")
                                st.metric("Risk & Momentum", f"{scores.risk_momentum:.1f}")
                                st.markdown(f"**Signal**: {signal}")
                            
                            st.markdown(framework.generate_recommendation(scores, {}))
        
        except Exception as e:
            st.error(f"❌ Error in financial analysis: {str(e)}")
            import traceback
            st.info(f"Debug Info:\n```\n{traceback.format_exc()}\n```")

# ============================================================================
# TAB 3: MARKET ANALYSIS
# ============================================================================

with tab3:
    st.subheader("📈 Market Analysis")
    
    st.info("📊 Analyzing price movements and technical metrics")
    
    try:
        all_data = fetch_all_company_data(period=selected_period)
        
        if all_data:
            # Candlestick charts
            st.subheader("📉 Candlestick Charts")
            
            for ticker, data in all_data.items():
                price_data = data.get('price_data')
                company_info = data.get('company_info', {})
                company_name = TICKERS.get(ticker, company_info.get('longName', ticker))
                
                if price_data is not None and not price_data.empty:
                    try:
                        # Handle MultiIndex
                        if isinstance(price_data.columns, pd.MultiIndex):
                            price_data.columns = price_data.columns.get_level_values(1)
                        
                        price_data.columns = price_data.columns.str.lower()
                        
                        if all(col in price_data.columns for col in ['open', 'high', 'low', 'close']):
                            fig = go.Figure(data=[go.Candlestick(
                                x=price_data.index,
                                open=price_data['open'],
                                high=price_data['high'],
                                low=price_data['low'],
                                close=price_data['close']
                            )])
                            
                            fig.update_layout(
                                title=f"{ticker} - {company_name}",
                                yaxis_title="Price ($)",
                                template="plotly_white",
                                height=400
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                    except:
                        st.warning(f"Could not display chart for {ticker}")
    
    except Exception as e:
        st.error(f"❌ Error in market analysis: {str(e)}")

# ============================================================================
# TAB 4: RISK ANALYSIS
# ============================================================================

with tab4:
    st.subheader("⚠️ Risk Analysis")
    
    st.info("Evaluating volatility, drawdown, and risk metrics")
    
    try:
        all_data = fetch_all_company_data(period=selected_period)
        
        if all_data:
            st.markdown("### Volatility Comparison")
            
            volatility_data = {}
            
            for ticker, data in all_data.items():
                price_data = data.get('price_data')
                
                if price_data is not None and not price_data.empty:
                    try:
                        if isinstance(price_data.columns, pd.MultiIndex):
                            price_data.columns = price_data.columns.get_level_values(1)
                        
                        price_data.columns = price_data.columns.str.lower()
                        
                        if 'close' in price_data.columns:
                            close_prices = price_data['close']
                        else:
                            close_prices = price_data.iloc[:, -1]
                        
                        returns = DataFetcher.calculate_returns(close_prices).dropna()
                        if not returns.empty:
                            volatility = DataFetcher.calculate_volatility(returns)
                            volatility_data[ticker] = volatility * 100
                    except:
                        pass
            
            if volatility_data:
                vol_df = pd.DataFrame(list(volatility_data.items()), columns=['Company', 'Volatility (%)'])
                vol_df = vol_df.sort_values('Volatility (%)', ascending=False)
                
                fig = go.Figure(data=[go.Bar(x=vol_df['Company'], y=vol_df['Volatility (%)'])])
                fig.update_layout(title="Annual Volatility Comparison", height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"❌ Error in risk analysis: {str(e)}")

# ============================================================================
# TAB 5: SUMMARY
# ============================================================================

with tab5:
    st.subheader("📋 Summary & Key Insights")
    
    st.markdown("""
    ### 📊 Analysis Summary
    
    This platform provides a comprehensive financial analysis of the top 5 US tech companies
    using the **Five-Lens Framework**.
    
    ### 🎯 Key Metrics
    
    - **Valuation Lens**: Assess if companies are fairly priced
    - **Quality Lens**: Evaluate business quality and profitability
    - **Growth Lens**: Analyze revenue and earnings growth
    - **Financial Health**: Review balance sheet strength and cash flow
    - **Risk & Momentum**: Evaluate volatility and market sentiment
    
    ### ⚠️ Important Notes
    
    1. **Educational Purpose**: This analysis is for learning only
    2. **Not Investment Advice**: Consult a financial advisor before investing
    3. **Past Performance**: Does not guarantee future results
    4. **Data Sources**: Yahoo Finance and public company information
    
    ---
    
    **For more information, visit The Mountain Path - World of Finance**
    
    Prof. V. Ravichandran
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
<p>© 2026 The Mountain Path - World of Finance</p>
<p>Prof. V. Ravichandran | 28+ Years Finance Experience</p>
</div>
""", unsafe_allow_html=True)
