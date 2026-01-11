
"""
Risk Analysis Module - VAR, CVAR, and Risk Metrics Calculations
Clean implementation with all required methods
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple


class RiskAnalyzer:
    """Calculate advanced risk metrics including VAR, CVAR, and Drawdown"""
    
    @staticmethod
    def calculate_var(returns: pd.Series, confidence: float = 0.95) -> float:
        """Calculate Value at Risk (VAR)"""
        try:
            if len(returns) == 0 or returns.empty:
                return 0.0
            var = np.percentile(returns, (1 - confidence) * 100)
            return var
        except:
            return 0.0
    
    @staticmethod
    def calculate_cvar(returns: pd.Series, confidence: float = 0.95) -> float:
        """Calculate Conditional Value at Risk (CVAR) / Expected Shortfall"""
        try:
            if len(returns) == 0 or returns.empty:
                return 0.0
            var = np.percentile(returns, (1 - confidence) * 100)
            cvar = returns[returns <= var].mean()
            return cvar if not np.isnan(cvar) else var
        except:
            return 0.0
    
    @staticmethod
    def calculate_sortino_ratio(returns: pd.Series, risk_free_rate: float = 0.04) -> float:
        """Calculate Sortino Ratio (only penalizes downside volatility)"""
        try:
            if len(returns) < 2:
                return 0.0
            
            annual_return = (returns.mean() * 252)
            negative_returns = returns[returns < 0]
            
            if len(negative_returns) == 0:
                downside_deviation = 0.0
            else:
                downside_deviation = negative_returns.std() * np.sqrt(252)
            
            if downside_deviation == 0:
                return 0.0
            
            sortino = (annual_return - risk_free_rate) / downside_deviation
            return sortino
        except:
            return 0.0
    
    @staticmethod
    def calculate_annual_volatility(returns: pd.Series) -> float:
        """Calculate annualized volatility"""
        try:
            if len(returns) < 2:
                return 0.0
            return returns.std() * np.sqrt(252)
        except:
            return 0.0
    
    @staticmethod
    def calculate_max_drawdown(prices: pd.Series) -> float:
        """Calculate Maximum Drawdown (MDD)"""
        try:
            if len(prices) < 2 or prices.empty:
                return 0.0
            
            running_max = prices.expanding().max()
            drawdown = (prices - running_max) / running_max
            max_dd = drawdown.min()
            
            return max_dd if not np.isnan(max_dd) else 0.0
        except:
            return 0.0
    
    @staticmethod
    def calculate_recovery_time(prices: pd.Series) -> int:
        """Calculate time to recovery from maximum drawdown"""
        try:
            if len(prices) < 2:
                return 0
            
            running_max = prices.expanding().max()
            drawdown = (prices - running_max) / running_max
            max_dd_idx = drawdown.idxmin()
            peak_before_dd = running_max.loc[max_dd_idx]
            prices_after_dd = prices.loc[max_dd_idx:]
            
            recovered = prices_after_dd[prices_after_dd >= peak_before_dd]
            
            if len(recovered) > 0:
                recovery_idx = recovered.index[0]
                recovery_days = (recovery_idx - max_dd_idx).days
                return max(0, recovery_days)
            else:
                return -1
        except:
            return 0
    
    @staticmethod
    def get_risk_assessment(var_95: float, cvar_95: float, volatility: float, sharpe: float) -> str:
        """Generate risk assessment based on metrics"""
        risk_score = 0
        
        vol_pct = volatility * 100
        if vol_pct < 15:
            risk_score += 1
        elif vol_pct < 20:
            risk_score += 2
        elif vol_pct < 30:
            risk_score += 3
        elif vol_pct < 40:
            risk_score += 4
        else:
            risk_score += 5
        
        var_pct = abs(var_95 * 100)
        if var_pct < 2:
            risk_score += 1
        elif var_pct < 3:
            risk_score += 2
        elif var_pct < 4:
            risk_score += 3
        elif var_pct < 5:
            risk_score += 4
        else:
            risk_score += 5
        
        if sharpe > 1.0:
            risk_score += 1
        elif sharpe > 0.5:
            risk_score += 2
        elif sharpe > 0:
            risk_score += 3
        else:
            risk_score += 4
        
        avg_score = risk_score / 3
        
        if avg_score < 2:
            return "🟢 Low Risk"
        elif avg_score < 3:
            return "🟡 Moderate Risk"
        elif avg_score < 3.5:
            return "🔴 High Risk"
        else:
            return "⚫ Very High Risk"
