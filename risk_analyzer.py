"""
Risk Analysis Module - VAR, CVAR, and Risk Metrics Calculations
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple


class RiskAnalyzer:
    """Calculate advanced risk metrics including VAR and CVAR"""
    
    @staticmethod
    def calculate_var(returns: pd.Series, confidence: float = 0.95) -> float:
        """
        Calculate Value at Risk (VAR)
        
        Parameters:
        -----------
        returns : pd.Series
            Daily returns
        confidence : float
            Confidence level (0.90, 0.95, 0.99)
        
        Returns:
        --------
        float
            VAR as a decimal (e.g., -0.05 for -5%)
        """
        try:
            if len(returns) == 0 or returns.empty:
                return 0.0
            
            var = np.percentile(returns, (1 - confidence) * 100)
            return var
        except Exception as e:
            print(f"Error calculating VAR: {e}")
            return 0.0
    
    @staticmethod
    def calculate_cvar(returns: pd.Series, confidence: float = 0.95) -> float:
        """
        Calculate Conditional Value at Risk (CVAR) / Expected Shortfall
        
        Parameters:
        -----------
        returns : pd.Series
            Daily returns
        confidence : float
            Confidence level (0.90, 0.95, 0.99)
        
        Returns:
        --------
        float
            CVAR as a decimal (e.g., -0.07 for -7%)
        """
        try:
            if len(returns) == 0 or returns.empty:
                return 0.0
            
            var = np.percentile(returns, (1 - confidence) * 100)
            cvar = returns[returns <= var].mean()
            
            return cvar if not np.isnan(cvar) else var
        except Exception as e:
            print(f"Error calculating CVAR: {e}")
            return 0.0
    
    @staticmethod
    def calculate_sortino_ratio(returns: pd.Series, risk_free_rate: float = 0.04) -> float:
        """
        Calculate Sortino Ratio (only penalizes downside volatility)
        
        Parameters:
        -----------
        returns : pd.Series
            Daily returns
        risk_free_rate : float
            Annual risk-free rate
        
        Returns:
        --------
        float
            Sortino ratio
        """
        try:
            if len(returns) < 2:
                return 0.0
            
            # Annualize returns and downside deviation
            annual_return = (returns.mean() * 252)
            
            # Downside deviation (only negative returns)
            negative_returns = returns[returns < 0]
            if len(negative_returns) == 0:
                downside_deviation = 0.0
            else:
                downside_deviation = negative_returns.std() * np.sqrt(252)
            
            if downside_deviation == 0:
                return 0.0
            
            sortino = (annual_return - risk_free_rate) / downside_deviation
            return sortino
        except Exception as e:
            print(f"Error calculating Sortino: {e}")
            return 0.0
    
    @staticmethod
    def calculate_annual_volatility(returns: pd.Series) -> float:
        """Calculate annualized volatility"""
        try:
            return returns.std() * np.sqrt(252)
        except:
            return 0.0
    
    @staticmethod
    def get_risk_assessment(var_95: float, cvar_95: float, volatility: float, sharpe: float) -> str:
        """
        Generate risk assessment based on metrics
        
        Parameters:
        -----------
        var_95 : float
            VAR at 95% confidence
        cvar_95 : float
            CVAR at 95% confidence
        volatility : float
            Annualized volatility
        sharpe : float
            Sharpe ratio
        
        Returns:
        --------
        str
            Risk assessment (Low, Moderate, High, Very High)
        """
        risk_score = 0
        
        # Volatility assessment
        vol_pct = volatility * 100
        if vol_pct < 20:
            risk_score += 1
        elif vol_pct < 30:
            risk_score += 2
        elif vol_pct < 40:
            risk_score += 3
        else:
            risk_score += 4
        
        # VAR assessment (worse = higher risk)
        var_pct = abs(var_95 * 100)
        if var_pct < 2:
            risk_score += 1
        elif var_pct < 3:
            risk_score += 2
        elif var_pct < 4:
            risk_score += 3
        else:
            risk_score += 4
        
        # Sharpe ratio (lower = higher risk)
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
    
    @staticmethod
    def generate_risk_metrics_dict(returns: pd.Series, annual_return: float, 
                                  confidence_levels: list = None) -> Dict:
        """
        Generate comprehensive risk metrics dictionary
        """
        if confidence_levels is None:
            confidence_levels = [0.90, 0.95, 0.99]
        
        volatility = RiskAnalyzer.calculate_annual_volatility(returns)
        sharpe = (annual_return - 0.04) / volatility if volatility > 0 else 0
        sortino = RiskAnalyzer.calculate_sortino_ratio(returns)
        
        metrics = {
            'annual_return': annual_return,
            'volatility': volatility,
            'sharpe_ratio': sharpe,
            'sortino_ratio': sortino,
        }
        
        # Add VAR and CVAR for each confidence level
        for conf in confidence_levels:
            conf_key = int(conf * 100)
            metrics[f'var_{conf_key}'] = RiskAnalyzer.calculate_var(returns, conf)
            metrics[f'cvar_{conf_key}'] = RiskAnalyzer.calculate_cvar(returns, conf)
        
        # Add risk assessment
        metrics['risk_assessment'] = RiskAnalyzer.get_risk_assessment(
            metrics['var_95'],
            metrics['cvar_95'],
            volatility,
            sharpe
        )
        
        return metrics
