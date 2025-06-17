import sys
import os

# Add the project root directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def get_investment_advice(overall_score, technical_indicators=None, fundamental_data=None, news_sentiment=None):
    """
    Generate investment advice based on the overall score and other factors.
    
    Args:
        overall_score (float): Overall stock score (0-10)
        technical_indicators (dict, optional): Technical indicators
        fundamental_data (dict, optional): Fundamental data
        news_sentiment (dict, optional): News sentiment data
    
    Returns:
        dict: Investment advice with recommendation and rationale
    """
    # Start with score-based recommendation
    recommendation = "HOLD"
    if overall_score >= config.BUY_THRESHOLD:
        recommendation = "BUY"
    elif overall_score <= config.SELL_THRESHOLD:
        recommendation = "SELL"
    elif overall_score < config.HOLD_THRESHOLD:
        recommendation = "DO NOTHING"
    
    # Build rationale
    rationale = []
    
    # Score-based rationale
    if overall_score >= 8.5:
        rationale.append("Very strong overall performance metrics.")
    elif overall_score >= 7.0:
        rationale.append("Good overall performance metrics.")
    elif overall_score <= 3.0:
        rationale.append("Poor overall performance metrics.")
    elif overall_score <= 4.5:
        rationale.append("Below average performance metrics.")
    else:
        rationale.append("Average overall performance metrics.")
    
    # Add technical indicators to rationale if available
    if technical_indicators:
        # RSI
        rsi = technical_indicators.get("rsi", 50)
        if rsi <= 30:
            rationale.append("RSI indicates oversold conditions.")
        elif rsi >= 70:
            rationale.append("RSI indicates overbought conditions.")
        
        # MACD
        if technical_indicators.get("macd_bullish_cross", False):
            rationale.append("Recent MACD bullish crossover suggests upward momentum.")
        elif technical_indicators.get("macd_bearish_cross", False):
            rationale.append("Recent MACD bearish crossover suggests downward momentum.")
        
        # Trend
        if technical_indicators.get("is_uptrend", False):
            if technical_indicators.get("strong_trend", False):
                rationale.append("Strong uptrend in price action.")
            else:
                rationale.append("Price is in an uptrend.")
        else:
            if technical_indicators.get("strong_trend", False):
                rationale.append("Strong downtrend in price action.")
            else:
                rationale.append("Price is in a downtrend.")
                
        # Support/Resistance
        if technical_indicators.get("near_support", False):
            rationale.append("Price is near support level, potential bounce point.")
        elif technical_indicators.get("near_resistance", False):
            rationale.append("Price is near resistance level, may face selling pressure.")
    
    # Add fundamental insights if available
    if fundamental_data:
        pe = fundamental_data.get("trailing_pe")
        if pe is not None:
            if pe < 0:
                rationale.append("Company has negative earnings (P/E).")
            elif pe < 15:
                rationale.append("P/E ratio suggests stock may be undervalued.")
            elif pe > 30:
                rationale.append("High P/E ratio may indicate overvaluation.")
        
        roe = fundamental_data.get("roe")
        if roe is not None:
            if roe > 0.15:
                rationale.append("Strong return on equity (ROE) indicates efficient use of capital.")
            elif roe < 0.05:
                rationale.append("Low return on equity (ROE) suggests inefficient use of capital.")
    
    # Add news sentiment if available
    if news_sentiment:
        avg_sentiment = news_sentiment.get("average_sentiment", 0)
        if avg_sentiment > 0.2:
            rationale.append("Recent news sentiment is very positive.")
        elif avg_sentiment > 0.05:
            rationale.append("Recent news sentiment is positive.")
        elif avg_sentiment < -0.2:
            rationale.append("Recent news sentiment is very negative.")
        elif avg_sentiment < -0.05:
            rationale.append("Recent news sentiment is negative.")
    
    # Override recommendation based on specific conditions
    if technical_indicators and fundamental_data:
        # Strong buy signals
        if (technical_indicators.get("is_oversold", False) and 
            technical_indicators.get("near_support", False) and 
            news_sentiment and news_sentiment.get("average_sentiment", 0) > 0.1):
            recommendation = "BUY"
            rationale.append("Oversold conditions with positive news make this a potential buying opportunity.")
            
        # Strong sell signals
        if (technical_indicators.get("is_overbought", False) and 
            technical_indicators.get("near_resistance", False) and 
            news_sentiment and news_sentiment.get("average_sentiment", 0) < -0.1):
            recommendation = "SELL"
            rationale.append("Overbought conditions with negative news suggest taking profits.")
    
    return {
        "recommendation": recommendation,
        "rationale": rationale
    }
