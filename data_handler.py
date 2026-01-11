
"""
Data Handler Module - Manages all data fetching with period selection
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import logging

# ============================================================================
# CONFIGURATION
# ============================================================================

TICKERS = ['NVDA', 'MSFT', 'AAPL', 'GOOGL', 'AMZN']
TRADING_DAYS_PER_YEAR = 252
RF_RATE_DEFAULT = 0.04  # 4% default risk-free rate

# ============================================================================
# LOGGING
# ============================================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# DATA FETCHER CLASS
# ============================================================================

class DataFetcher:
    """Main class for fetching and processing stock data"""
    
    @staticmethod
    @st.cache_data(ttl=3600)
    def fetch_stock_data(symbol, period="3y"):
        """
        Fetch stock price data from Yahoo Finance
        
        Args:
            symbol (str): Stock ticker
            period (str): Data period ("1y", "2y", "3y")
        
        Returns:
            pd.DataFrame: Price data with OHLCV
        """
        try:
            data = yf.download(symbol, period=period, progress=False)
            return data
        except Exception as e:
            logger.error(f"Error fetching {symbol}: {e}")
            return None
    
    @staticmethod
    def calculate_returns(prices):
        """Calculate daily returns"""
        try:
            if prices is None or len(prices) < 2:
                return pd.Series()
            return prices.pct_change()
        except:
            return pd.Series()
    
    @staticmethod
    def calculate_annual_return(prices):
        """Calculate annualized return"""
        try:
            if prices is None or len(prices) < 2:
                return 0.0
            start_price = prices.iloc[0]
            end_price = prices.iloc[-1]
            total_return = (end_price - start_price) / start_price
            years = len(prices) / TRADING_DAYS_PER_YEAR
            annual_return = (1 + total_return) ** (1 / years) - 1
            return annual_return
        except:
            return 0.0
    
    @staticmethod
    def calculate_volatility(returns):
        """Calculate daily volatility"""
        try:
            if returns is None or len(returns) < 2:
                return 0.0
            return returns.std()
        except:
            return 0.0
    
    @staticmethod
    def calculate_sharpe_ratio(returns, risk_free_rate=RF_RATE_DEFAULT):
        """Calculate Sharpe Ratio"""
        try:
            if len(returns) < 2:
                return 0.0
            annual_return = returns.mean() * TRADING_DAYS_PER_YEAR
            annual_volatility = returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)
            if annual_volatility == 0:
                return 0.0
            return (annual_return - risk_free_rate) / annual_volatility
        except:
            return 0.0
    
    @staticmethod
    def calculate_max_drawdown(prices):
        """Calculate maximum drawdown"""
        try:
            if prices is None or len(prices) < 2:
                return 0.0
            running_max = prices.expanding().max()
            drawdown = (prices - running_max) / running_max
            return drawdown.min()
        except:
            return 0.0


# ============================================================================
# DATA FETCHING FUNCTIONS
# ============================================================================

def fetch_all_company_data(period="3y"):
    """
    Fetch data for all companies
    
    Args:
        period (str): Data period - "1y", "2y", or "3y"
    
    Returns:
        dict: Data for all companies
    """
    all_data = {}
    
    for ticker in TICKERS:
        try:
            # Fetch price data
            price_data = DataFetcher.fetch_stock_data(ticker, period=period)
            
            # Fetch company info
            stock = yf.Ticker(ticker)
            company_info = stock.info
            
            all_data[ticker] = {
                'price_data': price_data,
                'company_info': company_info
            }
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {e}")
            all_data[ticker] = {
                'price_data': None,
                'company_info': {}
            }
    
    return all_data


def fetch_market_data(period="3y"):
    """
    Fetch market index data (S&P 500)
    
    Args:
        period (str): Data period - "1y", "2y", or "3y"
    
    Returns:
        pd.DataFrame: Market data
    """
    try:
        market_data = yf.download('^GSPC', period=period, progress=False)
        return market_data
    except Exception as e:
        logger.error(f"Error fetching market data: {e}")
        return None


def get_company_data(ticker, period="3y"):
    """
    Get data for single company
    
    Args:
        ticker (str): Stock ticker
        period (str): Data period - "1y", "2y", or "3y"
    
    Returns:
        dict: Company data
    """
    try:
        price_data = DataFetcher.fetch_stock_data(ticker, period=period)
        stock = yf.Ticker(ticker)
        company_info = stock.info
        
        return {
            'price_data': price_data,
            'company_info': company_info
        }
    except Exception as e:
        logger.error(f"Error fetching data for {ticker}: {e}")
        return {
            'price_data': None,
            'company_info': {}
        }
