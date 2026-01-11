"""
Configuration Module - Centralized settings for the entire application
Purpose: Single source of truth for all constants, avoiding hardcoding
"""

import os
from datetime import datetime, timedelta

# ============================================================================
# APPLICATION METADATA
# ============================================================================
APP_TITLE = "US Tech Companies Performance Analysis"
APP_SUBTITLE = "3-Year Rolling Window Analysis"
APP_VERSION = "1.0.0"
AUTHOR = "Prof. V. Ravichandran"
AUTHOR_DETAIL = "28+ Years Corporate Finance & Banking, 10+ Years Academic"

# ============================================================================
# DATA CONFIGURATION
# ============================================================================
TICKERS = {
    'NVDA': 'NVIDIA Corporation',
    'MSFT': 'Microsoft Corporation',
    'AAPL': 'Apple Inc.',
    'GOOGL': 'Alphabet Inc. (Google)',
    'AMZN': 'Amazon.com Inc.'
}

TICKER_LIST = list(TICKERS.keys())
TICKER_COLORS = {
    'NVDA': '#76B900',   # NVIDIA green
    'MSFT': '#00A4EF',   # Microsoft blue
    'AAPL': '#555555',   # Apple gray
    'GOOGL': '#4285F4',  # Google blue
    'AMZN': '#FF9900'    # Amazon orange
}

# Historical data settings
DATA_PERIOD = '3y'  # 3 years of daily data
DATA_INTERVAL = '1d'  # Daily
DATA_START_DATE = datetime.now() - timedelta(days=3*365)
DATA_END_DATE = datetime.now()

# Risk-free rate source
RF_RATE_SOURCE = 'FRED'  # Federal Reserve Economic Data
RF_RATE_TICKER = 'DGS10'  # 10-Year Treasury Yield
RF_RATE_DEFAULT = 0.0425  # 4.25% as fallback

# ============================================================================
# CACHING & PERFORMANCE
# ============================================================================
CACHE_TTL_HOURS = 4  # Cache validity: 4 hours
CACHE_TTL_SECONDS = CACHE_TTL_HOURS * 3600

# Scheduled data refresh (off-peak)
DATA_REFRESH_TIME = "04:30"  # 4:30 AM UTC = 11:30 PM EST
DATA_REFRESH_FREQUENCY_HOURS = 4  # Refresh every 4 hours

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2

# Rate limiting for API calls
RATE_LIMIT_MAX_REQUESTS = 2000
RATE_LIMIT_WINDOW_DAYS = 1
REQUEST_THROTTLE_SECONDS = 1  # Delay between requests

# ============================================================================
# STREAMLIT UI CONFIGURATION
# ============================================================================
PAGE_CONFIG = {
    "page_title": APP_TITLE,
    "page_icon": "📈",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Color scheme - Mountain Path theme
COLORS = {
    'primary': '#003366',      # Dark blue
    'secondary': '#004d80',    # Light blue
    'accent': '#FFD700',       # Gold
    'background': '#F5F7FA',   # Light background
    'text': '#212121',         # Dark text
    'success': '#4CAF50',
    'warning': '#FF9800',
    'error': '#F44336',
}

# ============================================================================
# RISK ANALYSIS PARAMETERS
# ============================================================================
# Confidence levels for VaR/CVaR
VaR_CONFIDENCE_LEVELS = [0.90, 0.95, 0.99]
VaR_DEFAULT_CONFIDENCE = 0.95

# Trading days per year (for annualization)
TRADING_DAYS_PER_YEAR = 252

# Performance benchmarks
BENCHMARK_SHARPE = 1.0       # Good: >1.0
BENCHMARK_SORTINO = 1.0      # Good: >1.0
BENCHMARK_VOLATILITY = 0.20  # 20% annual volatility threshold

# ============================================================================
# FILE PATHS & DATABASE
# ============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
BACKUP_DIR = os.path.join(DATA_DIR, 'backup')
DB_PATH = os.path.join(DATA_DIR, 'price_cache.db')
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# ============================================================================
# CONTACT & SOCIAL LINKS
# ============================================================================
LINKEDIN_URL = "https://www.linkedin.com/in/trichyravis/"
GITHUB_URL = "https://github.com/trichyravis"

# ============================================================================
# DISCLAIMER TEXT
# ============================================================================
DISCLAIMER = """
⚠️ **DISCLAIMER:** 

This tool is for **educational purposes only**. It is **NOT financial advice**.

• Always consult with a qualified financial advisor before making investment decisions
• Past performance does not guarantee future results
• This tool does not include taxes, fees, or transaction costs
• Data sourced from Yahoo Finance; may have delays or inaccuracies
• Risk metrics based on historical data; not predictive of future risk
• Markets are highly dynamic; analysis provides point-in-time snapshot only

**Use at your own risk. The Mountain Path - World of Finance assumes no liability.**
"""

# ============================================================================
# METHODOLOGY NOTES
# ============================================================================
METHODOLOGY = {
    'sharpe_ratio': 'Excess annual return / Annual volatility. Higher is better.',
    'sortino_ratio': 'Like Sharpe, but penalizes downside volatility only.',
    'var': 'Value-at-Risk: Worst expected loss at confidence level (e.g., 95%)',
    'cvar': 'Conditional VaR: Average loss beyond VaR threshold.',
    'max_drawdown': 'Maximum peak-to-trough decline over analysis period.',
    'volatility': 'Daily returns standard deviation, annualized (×√252)',
}

# ============================================================================
# EXPORT & REPORT SETTINGS
# ============================================================================
EXPORT_FORMAT = 'PDF'  # Future: also support Excel, HTML
REPORT_FONT_SIZE = 10
REPORT_PAGE_SIZE = 'A4'
