
"""
Data Handler Module - Manages all data fetching, caching, and validation
Purpose: Single source for data acquisition with fallback mechanisms
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import requests
import sqlite3
import logging
from datetime import datetime, timedelta
from config import (
    TICKERS, DATA_PERIOD, DATA_INTERVAL, CACHE_TTL_SECONDS,
    MAX_RETRIES, RETRY_DELAY_SECONDS, RF_RATE_SOURCE, RF_RATE_TICKER,
    RF_RATE_DEFAULT, DB_PATH, BACKUP_DIR, LOG_DIR, TRADING_DAYS_PER_YEAR
)
import time

# ============================================================================
# LOGGING SETUP
# ============================================================================
logging.basicConfig(
    filename=f'{LOG_DIR}/data_handler.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# DATABASE INITIALIZATION & MANAGEMENT
# ============================================================================

def initialize_database():
    """
    Initialize SQLite database with required tables
    Creates tables for price cache and metadata if they don't exist
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create price cache table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            date DATE NOT NULL,
            open REAL,
            high REAL,
            low REAL,
            close REAL NOT NULL,
            adj_close REAL,
            volume INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(ticker, date)
        )
        ''')
        
        # Create metadata table for update tracking
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS metadata (
            ticker TEXT PRIMARY KEY,
            last_update TIMESTAMP,
            records_count INTEGER,
            data_quality_score REAL
        )
        ''')
        
        # Create indices for faster queries
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ticker_date ON price_cache(ticker, date)')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")


# ============================================================================
# PRIMARY DATA FETCHING
# ============================================================================

@st.cache_data(ttl=CACHE_TTL_SECONDS)
def fetch_risk_free_rate():
    """
    Fetch current 10-Year US Treasury Yield (risk-free rate)
    Returns float or default value if API fails
    
    Returns:
        float: Risk-free rate as decimal (e.g., 0.0425 for 4.25%)
    """
    try:
        # Method 1: FRED API (most reliable) - direct HTTP request
        fred_url = f"https://fred.stlouisfed.org/data/{RF_RATE_TICKER}.json"
        response = requests.get(fred_url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            # Get the most recent data point
            observations = data.get('observations', [])
            if observations:
                latest_value = observations[-1].get('value')
                if latest_value and latest_value != '.':
                    rf_rate = float(latest_value) / 100  # Convert % to decimal
                    logger.info(f"Risk-free rate fetched from FRED: {rf_rate:.4f}")
                    return rf_rate
    except Exception as e:
        logger.warning(f"FRED API failed: {e}. Trying yfinance...")
    
    try:
        # Method 2: Fallback to yfinance TNX (10Y Yield)
        tnx_data = yf.download('^TNX', period='1d', progress=False)
        if not tnx_data.empty:
            rf_rate = tnx_data['Close'].iloc[-1] / 100
            logger.info(f"Risk-free rate fetched from yfinance: {rf_rate:.4f}")
            return rf_rate
    except Exception as e:
        logger.error(f"All RF rate sources failed: {e}. Using default.")
    
    return RF_RATE_DEFAULT


def fetch_stock_price_data_robust(ticker, max_retries=MAX_RETRIES):
    """
    Fetch historical stock price data with retry logic and fallback mechanisms
    
    Args:
        ticker (str): Stock ticker (e.g., 'NVDA')
        max_retries (int): Number of retry attempts
    
    Returns:
        pd.DataFrame: OHLCV data or None if all methods fail
    """
    for attempt in range(max_retries):
        try:
            data = yf.download(
                ticker,
                period=DATA_PERIOD,
                interval=DATA_INTERVAL,
                progress=False,
                prepost=False
            )
            
            if data.empty:
                raise ValueError(f"No data returned for {ticker}")
            
            # Rename columns to lowercase for consistency
            data.columns = data.columns.str.lower()
            
            logger.info(f"Successfully fetched {len(data)} records for {ticker}")
            return data
            
        except (ConnectionError, TimeoutError) as e:
            wait_time = RETRY_DELAY_SECONDS ** (attempt + 1)
            logger.warning(
                f"Attempt {attempt+1}/{max_retries} failed for {ticker}: {e}. "
                f"Retrying in {wait_time}s..."
            )
            time.sleep(wait_time)
        
        except Exception as e:
            logger.error(f"Unexpected error for {ticker}: {e}")
            break
    
    # All retries exhausted - try fallback mechanisms
    logger.warning(f"All fetch attempts failed for {ticker}. Checking SQLite cache...")
    cached_data = load_from_sqlite(ticker)
    
    if cached_data is not None and not cached_data.empty:
        logger.info(f"Loaded {len(cached_data)} records from cache for {ticker}")
        return cached_data
    
    # Final fallback: CSV backup
    logger.warning(f"Cache empty for {ticker}. Trying CSV backup...")
    backup_data = load_from_csv(ticker)
    
    if backup_data is not None:
        logger.info(f"Loaded {len(backup_data)} records from CSV for {ticker}")
        return backup_data
    
    logger.error(f"All data sources exhausted for {ticker}")
    return None


# ============================================================================
# CACHE MANAGEMENT
# ============================================================================

def save_to_sqlite(ticker, data):
    """
    Persist stock price data to SQLite cache
    
    Args:
        ticker (str): Stock ticker
        data (pd.DataFrame): OHLCV data
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        
        # Reset index to include date as column
        data_to_save = data.reset_index()
        data_to_save['ticker'] = ticker
        
        # Insert/replace data (UNIQUE constraint on ticker, date)
        data_to_save.to_sql('price_cache', conn, if_exists='append', index=False)
        
        # Update metadata
        cursor = conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO metadata (ticker, last_update, records_count, data_quality_score)
        VALUES (?, ?, ?, ?)
        ''', (ticker, datetime.now(), len(data), 0.95))
        
        conn.commit()
        conn.close()
        logger.info(f"Saved {len(data)} records for {ticker} to SQLite")
        
    except Exception as e:
        logger.error(f"Failed to save {ticker} to SQLite: {e}")


def load_from_sqlite(ticker):
    """
    Load stock price data from SQLite cache
    
    Args:
        ticker (str): Stock ticker
    
    Returns:
        pd.DataFrame or None
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        query = f"""
        SELECT date, open, high, low, close, adj_close, volume 
        FROM price_cache 
        WHERE ticker = '{ticker}' 
        ORDER BY date DESC 
        LIMIT {TRADING_DAYS_PER_YEAR * 3}
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            return None
        
        # Convert date to datetime and set as index
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        df = df.sort_index()
        
        # Rename columns to match yfinance format
        df.columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        
        logger.info(f"Loaded {len(df)} records for {ticker} from SQLite")
        return df
        
    except Exception as e:
        logger.error(f"Failed to load {ticker} from SQLite: {e}")
        return None


def load_from_csv(ticker):
    """
    Load stock price data from CSV backup
    
    Args:
        ticker (str): Stock ticker
    
    Returns:
        pd.DataFrame or None
    """
    try:
        filepath = f'{BACKUP_DIR}/{ticker}_3y_backup.csv'
        df = pd.read_csv(filepath, index_col=0, parse_dates=True)
        logger.info(f"Loaded {len(df)} records for {ticker} from CSV")
        return df
    except FileNotFoundError:
        logger.warning(f"No CSV backup found for {ticker}")
        return None
    except Exception as e:
        logger.error(f"Failed to load {ticker} from CSV: {e}")
        return None


# ============================================================================
# DATA VALIDATION
# ============================================================================

def validate_data_quality(df, ticker):
    """
    Validate data quality and flag issues
    
    Args:
        df (pd.DataFrame): OHLCV data
        ticker (str): Stock ticker
    
    Returns:
        dict: Validation results {issue: severity}
    """
    issues = {}
    
    if df is None or df.empty:
        return {'empty_data': 'Critical'}
    
    # Check for missing values
    missing_pct = df.isnull().sum().sum() / (df.size) * 100 if df.size > 0 else 0
    if missing_pct > 5:
        issues['missing_values'] = f"High: {missing_pct:.1f}% missing"
    
    # Check for stale data
    if (datetime.now() - df.index[-1]).days > 2:
        issues['stale_data'] = f"Data is {(datetime.now() - df.index[-1]).days} days old"
    
    # Log issues
    if issues:
        logger.warning(f"{ticker} data issues: {issues}")
    else:
        logger.info(f"{ticker} passed data quality checks")
    
    return issues


# ============================================================================
# DATA RETRIEVAL WRAPPER (PUBLIC INTERFACE)
# ============================================================================

def get_all_stock_data():
    """
    Fetch data for all tickers with caching
    
    Returns:
        dict: {ticker: DataFrame}
    """
    all_data = {}
    
    for ticker in TICKERS.keys():
        data = fetch_stock_price_data_robust(ticker)
        if data is not None:
            # Validate & save to cache
            issues = validate_data_quality(data, ticker)
            save_to_sqlite(ticker, data)
            all_data[ticker] = data
        else:
            st.warning(f"⚠️ Could not fetch data for {ticker}. Using cached data...")
            cached_data = load_from_sqlite(ticker)
            if cached_data is not None:
                all_data[ticker] = cached_data
    
    return all_data


@st.cache_data(ttl=CACHE_TTL_SECONDS)
def get_stock_data(ticker):
    """
    Get stock data for single ticker with caching
    
    Args:
        ticker (str): Stock ticker
    
    Returns:
        pd.DataFrame or None
    """
    data = fetch_stock_price_data_robust(ticker)
    if data is not None:
        save_to_sqlite(ticker, data)
        return data
    else:
        return load_from_sqlite(ticker)


# ============================================================================
# INITIALIZATION
# ============================================================================

def initialize_data_handler():
    """Call on app startup to set up database"""
    initialize_database()
    logger.info("Data handler initialized")
