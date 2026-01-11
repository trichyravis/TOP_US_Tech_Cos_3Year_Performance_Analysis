# US Tech Companies Performance Analysis - Streamlit App

A comprehensive 3-year performance analysis dashboard for top US technology companies (NVIDIA, Microsoft, Apple, Alphabet, Amazon) using Streamlit, Python, and financial analytics.

## 🎯 Features

- **📊 Interactive Dashboard:** 5 comprehensive tabs with real-time data
- **💰 Financial Analysis:** Revenue, operating income, net income trends
- **📈 Market Analysis:** Stock prices, returns, volatility, correlations
- **⚠️ Risk Assessment:** Sharpe ratio, Sortino ratio, VaR, CVaR, Max Drawdown
- **🔄 Auto-Update:** Data refreshes every 4 hours automatically
- **🎨 Professional Branding:** Mountain Path - World of Finance theme

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Technologies](#-technologies)
- [Data Sources](#-data-sources)
- [Disclaimer](#-disclaimer)
- [Contact](#-contact)

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Setup Steps

1. **Clone the repository:**
```bash
git clone https://github.com/trichyravis/us_tech_analysis_app.git
cd us_tech_analysis_app
```

2. **Create virtual environment:**
```bash
# macOS/Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the app:**
```bash
streamlit run main.py
```

5. **Open in browser:**
Visit `http://localhost:8501` to view the application

## 💻 Usage

### Navigating the App

**Tab 1: About Platform**
- Overview of the platform
- Data sources and update frequency
- Contact information
- Disclaimer and methodology

**Tab 2: Financial Performance**
- Company financial metrics (Revenue, Income, Margins)
- Single company or all companies comparison
- 3-year price trends

**Tab 3: Market Analysis**
- Stock price candlestick charts
- Annual returns comparison
- Volatility analysis
- Correlation matrix

**Tab 4: Risk Analysis**
- Risk metrics dashboard (Sharpe, Sortino, VaR, CVaR, Max DD)
- Risk metrics heatmap
- VaR visualization at different confidence levels
- Risk-adjusted performance ranking

**Tab 5: Summary & Insights**
- Executive summary with key findings
- Performance rankings by different metrics
- Comprehensive comparison table
- Best/worst performers

### Customizing Filters

Most tabs allow you to:
- Select individual companies or compare multiple
- Choose analysis dates
- Adjust confidence levels for risk metrics

## 📁 Project Structure

```
us_tech_analysis_app/
├── main.py                      # Main Streamlit app entry point
├── config.py                    # Configuration constants
├── styles.py                    # Branding and CSS styling
├── components.py                # Reusable UI components
├── data_handler.py             # Data fetching and caching
├── analytics.py                # Financial calculations
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml             # Streamlit configuration
├── .gitignore                  # Git ignore file
├── README.md                   # This file
├── data/                       # Data storage (auto-created)
│   ├── price_cache.db          # SQLite cache
│   └── backup/                 # CSV backups
└── logs/                       # Application logs (auto-created)
    └── data_handler.log        # Data handler logs
```

## 🛠 Technologies

### Backend
- **Streamlit:** Web application framework
- **Pandas:** Data manipulation and analysis
- **NumPy:** Numerical computations
- **yfinance:** Yahoo Finance data fetching
- **pandas_datareader:** Federal Reserve data (Treasury yields)
- **SQLite:** Data caching database
- **Plotly:** Interactive visualizations

### Development
- **Python 3.8+**
- **Git:** Version control
- **Virtual Environment:** Dependency isolation

## 📊 Data Sources

| Source | Data | Update Frequency |
|--------|------|------------------|
| Yahoo Finance | Daily Stock Prices (OHLCV) | Every 4 hours |
| Yahoo Finance | Annual Financial Data | Daily |
| Federal Reserve (FRED) | 10-Year Treasury Yield | Daily |

### Companies Analyzed
- **NVDA:** NVIDIA Corporation (AI & Semiconductors)
- **MSFT:** Microsoft Corporation (Cloud & Software)
- **AAPL:** Apple Inc. (Consumer Electronics)
- **GOOGL:** Alphabet Inc. (Digital Advertising)
- **AMZN:** Amazon.com Inc. (E-commerce & Cloud)

## 🔐 Data & Caching

The app uses a 3-layer caching strategy for optimal performance and reliability:

1. **Layer 1:** Streamlit session cache (in-memory, 4-hour TTL)
2. **Layer 2:** SQLite persistent database
3. **Layer 3:** CSV backup files

This ensures data availability even if external APIs are temporarily unavailable.

## ⚠️ Disclaimer

**Educational Purpose Only:**
- This tool is for educational purposes only
- NOT financial advice
- Always consult a qualified financial advisor before making investment decisions
- Past performance does not guarantee future results
- This tool does not include taxes, fees, or transaction costs
- Data may have delays or inaccuracies
- Risk metrics are based on historical data and not predictive

**Use at your own risk.** The Mountain Path - World of Finance assumes no liability for any financial decisions made using this tool.

## 🧮 Metrics Explained

### Risk Metrics

**Sharpe Ratio**
- Measures risk-adjusted returns
- Formula: (Annual Return - Risk-Free Rate) / Annual Volatility
- Interpretation: Higher is better (>1.0 is good)

**Sortino Ratio**
- Like Sharpe but penalizes downside volatility only
- Better for non-normal distributions
- Interpretation: Higher is better (>1.0 is good)

**Value-at-Risk (VaR)**
- Worst expected loss at a given confidence level (95% or 99%)
- Shows potential daily loss on the portfolio

**Conditional VaR (CVaR)**
- Expected Shortfall: average loss beyond VaR threshold
- Measures tail risk

**Maximum Drawdown**
- Largest peak-to-trough decline during the period
- Measures historical volatility and risk

## 🔄 Automated Updates

Data automatically refreshes every 4 hours using GitHub Actions (when deployed).

For local development, click the "🔄 Refresh Data" button in the sidebar to manually update.

## 📈 Performance Targets

- Page Load Time: <3 seconds
- Data Freshness: <4 hours old
- API Success Rate: >98%
- Uptime: >99.5%

## 🐛 Troubleshooting

### "Rate limit exceeded"
- yfinance has a daily limit of 2000 requests
- Solution: Data is cached for 4 hours to avoid hitting this limit

### "No data for ticker"
- Check your internet connection
- Verify ticker symbols are correct
- Try clicking "Refresh Data" button

### "Memory error"
- On Streamlit Cloud, data is compressed for efficiency
- Consider reducing history to 2 years if issues persist

### "Slow performance"
- First load will be slower (data fetching)
- Subsequent loads use cached data (fast)
- Try reducing the date range for analysis

## 📞 Contact & Resources

**Author:** Prof. V. Ravichandran
- **Experience:** 28+ Years Corporate Finance & Banking, 10+ Years Academic Excellence
- **LinkedIn:** [trichyravis](https://www.linkedin.com/in/trichyravis/)
- **GitHub:** [trichyravis](https://github.com/trichyravis)

## 📄 License

This project is provided as-is for educational purposes. 

## 🚀 Deployment

### Deploy to Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Click "New app" and select your repository
4. Set main file to `main.py`
5. Deploy!

### Deploy to Docker

```bash
docker build -t us-tech-analysis .
docker run -p 8501:8501 us-tech-analysis
```

## 🎓 Educational Use

This platform is designed for:
- MBA students studying financial analysis
- CFA candidates learning risk management
- FRM professionals exploring quantitative finance
- Finance educators building curriculum
- Individual investors learning about markets

## 🙏 Acknowledgments

- Yahoo Finance for stock price data
- Federal Reserve Economic Data (FRED) for Treasury yields
- Streamlit for the amazing web framework
- The open-source Python community

---

**Last Updated:** January 11, 2025  
**Version:** 1.0.0  
**Status:** Active Development

For issues, questions, or suggestions, please open a GitHub issue or reach out directly.

Happy analyzing! 📊📈
