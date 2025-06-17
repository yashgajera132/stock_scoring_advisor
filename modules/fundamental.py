import sys
import os
import numpy as np

# Add the project root directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def analyze_fundamental(fundamental_data, sector_avg=None):
    """
    Analyze fundamental data to produce a score.
    
    Args:
        fundamental_data (dict): Fundamental metrics
        sector_avg (dict, optional): Sector average metrics for comparison
    
    Returns:
        float: Fundamental analysis score (0-10)
    """
    if not fundamental_data:
        return 5.0  # Neutral score if no data
    
    try:
        score = 5.0  # Start from neutral position
        
        # PE Ratio analysis
        pe = fundamental_data.get("trailing_pe")
        if pe is not None:
            if pe < 0:  # Negative earnings
                score -= 0.5
            elif pe < 15:  # Potentially undervalued
                score += 1.0
            elif pe > 30:  # Potentially overvalued
                score -= 0.5
                
        # Forward PE analysis
        forward_pe = fundamental_data.get("forward_pe")
        if forward_pe is not None and pe is not None:
            if forward_pe < pe:  # Expecting improved earnings
                score += 0.5
            elif forward_pe > pe:  # Expecting worse earnings
                score -= 0.5
                
        # Price to Book analysis
        pb = fundamental_data.get("price_to_book")
        if pb is not None:
            if pb < 1.0:  # Potentially undervalued
                score += 0.75
            elif pb > 5.0:  # Potentially overvalued
                score -= 0.5
                
        # Return on Equity
        roe = fundamental_data.get("roe")
        if roe is not None:
            if roe > 0.15:  # Good ROE
                score += 1.0
            elif roe < 0.05:  # Poor ROE
                score -= 0.75
                
        # Profit Margins
        profit_margins = fundamental_data.get("profit_margins")
        if profit_margins is not None:
            if profit_margins > 0.15:  # High margins
                score += 0.75
            elif profit_margins < 0.05:  # Low margins
                score -= 0.5
                
        # Dividend Yield
        div_yield = fundamental_data.get("dividend_yield")
        if div_yield is not None:
            if div_yield > 0.04:  # High dividend
                score += 0.5
            elif div_yield > 0 and div_yield < 0.01:  # Low dividend
                score -= 0.25
                
        # Debt to Equity
        debt_to_equity = fundamental_data.get("debt_to_equity")
        if debt_to_equity is not None:
            if debt_to_equity > 2.0:  # High debt
                score -= 1.0
            elif debt_to_equity < 0.5:  # Low debt
                score += 0.75
                
        # Liquidity - Current Ratio
        current_ratio = fundamental_data.get("current_ratio")
        if current_ratio is not None:
            if current_ratio < 1.0:  # Poor liquidity
                score -= 0.75
            elif current_ratio > 2.0:  # Strong liquidity
                score += 0.5
                
        # Beta (volatility)
        beta = fundamental_data.get("beta")
        if beta is not None:
            if beta > 1.5:  # High volatility
                score -= 0.25
            elif beta < 0.8:  # Low volatility
                score += 0.25
                
        # Ensure score is within bounds
        return max(0, min(score, 10))
    except Exception as e:
        print(f"Error analyzing fundamental data: {e}")
        return 5.0  # Return neutral score on error
