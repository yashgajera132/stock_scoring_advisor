import numpy as np
import sys
import os

# Add the project root directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def calculate_overall_score(technical_score, fundamental_score, news_sentiment_score):
    """
    Calculate the overall stock score based on technical, fundamental and news sentiment analysis.
    
    Args:
        technical_score (float): Technical analysis score (0-10)
        fundamental_score (float): Fundamental analysis score (0-10)
        news_sentiment_score (float): News sentiment score (0-10)
    
    Returns:
        float: Overall stock score (0-10)
    """
    # Apply weights from config
    weighted_score = (
        technical_score * config.TECHNICAL_WEIGHT +
        fundamental_score * config.FUNDAMENTAL_WEIGHT +
        news_sentiment_score * config.NEWS_SENTIMENT_WEIGHT
    )
    
    # Round to 1 decimal place
    return round(weighted_score, 1)

def get_score_components(technical_indicators, fundamental_data, news_sentiment):
    """
    Get the component scores and descriptions.
    
    Args:
        technical_indicators (dict): Technical indicators
        fundamental_data (dict): Fundamental data
        news_sentiment (dict): News sentiment data
    
    Returns:
        dict: Component scores and explanations
    """
    components = {
        "technical": {
            "score": 0,
            "factors": []
        },
        "fundamental": {
            "score": 0,
            "factors": []
        },
        "news_sentiment": {
            "score": 0,
            "factors": []
        }
    }
    
    # Technical Factors
    if technical_indicators:
        rsi = technical_indicators.get("rsi", 0)
        components["technical"]["factors"].append({
            "name": "RSI",
            "value": round(rsi, 2),
            "interpretation": "Oversold" if rsi < 30 else "Overbought" if rsi > 70 else "Neutral"
        })
        
        if technical_indicators.get("macd_bullish_cross", False):
            components["technical"]["factors"].append({
                "name": "MACD",
                "value": "Bullish Crossover",
                "interpretation": "Positive"
            })
        elif technical_indicators.get("macd_bearish_cross", False):
            components["technical"]["factors"].append({
                "name": "MACD",
                "value": "Bearish Crossover",
                "interpretation": "Negative"
            })
            
        components["technical"]["factors"].append({
            "name": "Trend",
            "value": "Uptrend" if technical_indicators.get("is_uptrend", False) else "Downtrend",
            "interpretation": "Positive" if technical_indicators.get("is_uptrend", False) else "Negative"
        })
        
        if technical_indicators.get("near_support", False):
            components["technical"]["factors"].append({
                "name": "Price Level",
                "value": "Near Support",
                "interpretation": "Potential Reversal Up"
            })
        elif technical_indicators.get("near_resistance", False):
            components["technical"]["factors"].append({
                "name": "Price Level",
                "value": "Near Resistance",
                "interpretation": "Potential Reversal Down"
            })
    
    # Fundamental Factors
    if fundamental_data:
        pe = fundamental_data.get("trailing_pe")
        if pe is not None:
            components["fundamental"]["factors"].append({
                "name": "P/E Ratio",
                "value": round(pe, 2) if pe > 0 else "Negative",
                "interpretation": "Undervalued" if pe > 0 and pe < 15 else "Overvalued" if pe > 30 else "Fair" if pe > 0 else "Unprofitable"
            })
            
        roe = fundamental_data.get("roe")
        if roe is not None:
            components["fundamental"]["factors"].append({
                "name": "ROE",
                "value": f"{round(roe * 100, 2)}%" if roe is not None else "N/A",
                "interpretation": "Good" if roe > 0.15 else "Poor" if roe < 0.05 else "Average"
            })
            
        debt_to_equity = fundamental_data.get("debt_to_equity")
        if debt_to_equity is not None:
            components["fundamental"]["factors"].append({
                "name": "Debt/Equity",
                "value": round(debt_to_equity, 2),
                "interpretation": "High Debt" if debt_to_equity > 2 else "Low Debt" if debt_to_equity < 0.5 else "Average"
            })
    
    # News Sentiment
    if news_sentiment:
        total_articles = news_sentiment.get("positive", 0) + news_sentiment.get("negative", 0) + news_sentiment.get("neutral", 0)
        if total_articles > 0:
            pos_percent = (news_sentiment.get("positive", 0) / total_articles) * 100
            neg_percent = (news_sentiment.get("negative", 0) / total_articles) * 100
            
            components["news_sentiment"]["factors"].append({
                "name": "Sentiment Distribution",
                "value": f"{news_sentiment.get('positive', 0)} positive, {news_sentiment.get('negative', 0)} negative",
                "interpretation": f"{round(pos_percent, 1)}% positive, {round(neg_percent, 1)}% negative"
            })
            
            components["news_sentiment"]["factors"].append({
                "name": "Average Sentiment",
                "value": round(news_sentiment.get("average_sentiment", 0), 2),
                "interpretation": "Positive" if news_sentiment.get("average_sentiment", 0) > 0.05 else 
                                 "Negative" if news_sentiment.get("average_sentiment", 0) < -0.05 else "Neutral"
            })
    
    return components
