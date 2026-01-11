"""
Analytics Module - Financial and risk metrics calculations
Purpose: Vectorized NumPy operations for all metrics
"""

import numpy as np
import pandas as pd
from config import TRADING_DAYS_PER_YEAR
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# RETURN CALCULATIONS
# ============================================================================

def calculate_returns(price_series, periods=1):
    """
    Calculate periodic returns from price series
    
    Args:
        price_series (pd.Series): Closing prices
        periods (int): Return period in days
    
    Returns:
        pd.Series: Periodic returns as decimals
    """
    return price_series.pct_change(periods=periods)


def calculate_annual_return(price_series):
    """
    Calculate annualized return over full period
    
    Args:
        price_series (pd.Series): Closing prices
    
    Returns:
        float: Annualized return as decimal
    """
    price_series = price_series.dropna()
    
    if len(price_series) < 2:
        return 0
    
    start_price = price_series.iloc[0]
    end_price = price_series.iloc[-1]
    num_years = len(price_series) / TRADING_DAYS_PER_YEAR
    
    if num_years == 0 or start_price == 0:
        return 0
    
    annual_return = (end_price / start_price) ** (1 / num_years) - 1
    return annual_return


# ============================================================================
# VOLATILITY & RISK METRICS
# ============================================================================

def calculate_volatility(returns, annualize=True):
    """
    Calculate volatility (standard deviation of returns)
    
    Args:
        returns (pd.Series): Daily returns
        annualize (bool): Annualize volatility if True
    
    Returns:
        float: Volatility as decimal
    """
    returns = returns.dropna()
    
    if len(returns) < 2:
        return 0
    
    volatility = returns.std()
    
    if annualize:
        volatility *= np.sqrt(TRADING_DAYS_PER_YEAR)
    
    return volatility


def calculate_sharpe_ratio(returns, rf_rate, annualize=True):
    """
    Calculate Sharpe Ratio
    Sharpe = (Annual Return - Risk-Free Rate) / Annual Volatility
    
    Args:
        returns (pd.Series): Daily returns
        rf_rate (float): Risk-free rate as decimal
        annualize (bool): Use annualized returns/volatility
    
    Returns:
        float: Sharpe ratio
    """
    returns = returns.dropna()
    
    if len(returns) < 2:
        return 0
    
    mean_return = returns.mean()
    volatility = returns.std()
    
    if annualize:
        mean_return *= TRADING_DAYS_PER_YEAR
        volatility *= np.sqrt(TRADING_DAYS_PER_YEAR)
    
    excess_return = mean_return - rf_rate
    
    if volatility == 0:
        return 0
    
    sharpe = excess_return / volatility
    return sharpe


def calculate_sortino_ratio(returns, rf_rate, target_return=0):
    """
    Calculate Sortino Ratio (downside volatility only)
    Better for non-normal distributions than Sharpe
    
    Args:
        returns (pd.Series): Daily returns
        rf_rate (float): Risk-free rate as decimal
        target_return (float): Target return threshold
    
    Returns:
        float: Sortino ratio
    """
    returns = returns.dropna()
    
    if len(returns) < 2:
        return 0
    
    excess_return = returns.mean() * TRADING_DAYS_PER_YEAR - rf_rate
    
    # Downside deviation: volatility of returns below target
    downside_returns = returns[returns < target_return]
    
    if len(downside_returns) == 0:
        return float('inf') if excess_return > 0 else 0
    
    downside_volatility = downside_returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)
    
    if downside_volatility == 0:
        return 0
    
    sortino = excess_return / downside_volatility
    return sortino


# ============================================================================
# VALUE-AT-RISK CALCULATIONS
# ============================================================================

def calculate_var_cvar(returns, confidence_level=0.95, holding_period=1):
    """
    Calculate Value-at-Risk (VaR) and Conditional VaR (CVaR/Expected Shortfall)
    Using historical simulation method
    
    Args:
        returns (pd.Series): Daily returns
        confidence_level (float): Confidence level (e.g., 0.95 for 95%)
        holding_period (int): Holding period in days
    
    Returns:
        tuple: (VaR, CVaR) as decimals
    """
    returns = returns.dropna()
    
    if len(returns) < 2:
        return 0, 0
    
    # Adjust returns for holding period
    hp_returns = returns.rolling(window=holding_period).sum()
    hp_returns = hp_returns.dropna()
    
    if len(hp_returns) == 0:
        return 0, 0
    
    # Calculate percentile (downside)
    percentile = (1 - confidence_level) * 100
    var = np.percentile(hp_returns, percentile)
    
    # CVaR: average of worst losses beyond VaR
    cvar = hp_returns[hp_returns <= var].mean()
    
    # Handle NaN
    if pd.isna(cvar):
        cvar = var
    
    return var, cvar


# ============================================================================
# MAXIMUM DRAWDOWN
# ============================================================================

def calculate_max_drawdown(price_series):
    """
    Calculate Maximum Drawdown
    Max DD = (Trough Value - Peak Value) / Peak Value
    
    Args:
        price_series (pd.Series): Closing prices
    
    Returns:
        float: Maximum drawdown as decimal (negative value)
    """
    price_series = price_series.dropna()
    
    if len(price_series) < 2:
        return 0
    
    # Calculate cumulative returns
    cumulative_returns = (1 + calculate_returns(price_series)).cumprod()
    
    # Running maximum
    running_max = cumulative_returns.expanding().max()
    
    # Drawdown at each point
    drawdown = (cumulative_returns - running_max) / running_max
    
    max_dd = drawdown.min()
    return max_dd


def calculate_rolling_drawdown(price_series, window=252):
    """
    Calculate rolling maximum drawdown (1-year window)
    
    Args:
        price_series (pd.Series): Closing prices
        window (int): Window size in days
    
    Returns:
        pd.Series: Rolling max drawdown
    """
    price_series = price_series.dropna()
    
    if len(price_series) < window:
        return pd.Series(dtype=float)
    
    cumulative_returns = (1 + calculate_returns(price_series)).cumprod()
    
    rolling_max = cumulative_returns.rolling(window=window).max()
    rolling_drawdown = (cumulative_returns - rolling_max) / rolling_max
    
    return rolling_drawdown.rolling(window=window).min()


# ============================================================================
# COMPARATIVE ANALYSIS
# ============================================================================

def calculate_correlation_matrix(price_data_dict):
    """
    Calculate correlation matrix for multiple stocks
    
    Args:
        price_data_dict (dict): {ticker: price_series, ...}
    
    Returns:
        pd.DataFrame: Correlation matrix
    """
    returns_dict = {}
    
    for ticker, prices in price_data_dict.items():
        returns = calculate_returns(prices)
        returns_dict[ticker] = returns
    
    returns_df = pd.DataFrame(returns_dict)
    correlation = returns_df.corr()
    
    return correlation


# ============================================================================
# SUMMARY METRICS
# ============================================================================

def generate_risk_summary(ticker, price_data, returns_data, rf_rate):
    """
    Generate comprehensive risk summary for a stock
    
    Args:
        ticker (str): Stock ticker
        price_data (pd.Series): Closing prices
        returns_data (pd.Series): Daily returns
        rf_rate (float): Risk-free rate
    
    Returns:
        dict: Risk metrics summary
    """
    annual_return = calculate_annual_return(price_data)
    volatility = calculate_volatility(returns_data)
    sharpe = calculate_sharpe_ratio(returns_data, rf_rate)
    sortino = calculate_sortino_ratio(returns_data, rf_rate)
    max_dd = calculate_max_drawdown(price_data)
    var_95, cvar_95 = calculate_var_cvar(returns_data, confidence_level=0.95)
    var_99, cvar_99 = calculate_var_cvar(returns_data, confidence_level=0.99)
    
    summary = {
        'ticker': ticker,
        'annual_return': annual_return,
        'annual_volatility': volatility,
        'sharpe_ratio': sharpe,
        'sortino_ratio': sortino,
        'max_drawdown': max_dd,
        'var_95': var_95,
        'cvar_95': cvar_95,
        'var_99': var_99,
        'cvar_99': cvar_99,
    }
    
    return summary
