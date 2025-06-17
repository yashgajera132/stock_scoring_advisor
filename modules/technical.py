import pandas as pd
import pandas_ta as ta
import numpy as np
import sys
import os

# Add the project root directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def calculate_technical_indicators(stock_data):
    """
    Calculate technical indicators for the stock.
    
    Args:
        stock_data (pd.DataFrame): DataFrame with stock price data
    
    Returns:
        dict: Technical indicators and their values
    """
    if stock_data.empty:
        return {}
    
    try:
        # Make a copy to avoid modifying the original
        df = stock_data.copy()
        
        # Calculate RSI
        df['rsi'] = ta.rsi(df['Close'], length=config.RSI_WINDOW)
        
        # Calculate MACD
        macd = ta.macd(df['Close'], 
                        fast=config.MACD_FAST, 
                        slow=config.MACD_SLOW, 
                        signal=config.MACD_SIGNAL)
        df = pd.concat([df, macd], axis=1)
        
        # Calculate Moving Averages
        df['ma_short'] = ta.sma(df['Close'], length=config.MA_SHORT)
        df['ma_long'] = ta.sma(df['Close'], length=config.MA_LONG)
        
        # Calculate Bollinger Bands
        bbands = ta.bbands(df['Close'], length=20, std=2)
        df = pd.concat([df, bbands], axis=1)
        
        # Check if prices are near support/resistance (Bollinger Bands)
        last_close = df['Close'].iloc[-1]
        last_lower_band = df['BBL_20_2.0'].iloc[-1]
        last_upper_band = df['BBU_20_2.0'].iloc[-1]
        
        # Determine if price is in an uptrend or downtrend based on MAs
        uptrend = df['ma_short'].iloc[-1] > df['ma_long'].iloc[-1]
        
        # Calculate volatility (Average True Range / Close price)
        df['atr'] = ta.atr(df['High'], df['Low'], df['Close'], length=14)
        volatility = (df['atr'].iloc[-1] / df['Close'].iloc[-1]) * 100
        
        # RSI conditions
        overbought = df['rsi'].iloc[-1] > config.RSI_OVERBOUGHT
        oversold = df['rsi'].iloc[-1] < config.RSI_OVERSOLD
        
        # MACD conditions
        macd_bull_cross = (df['MACD_12_26_9'].iloc[-2] < df['MACDs_12_26_9'].iloc[-2]) and \
                          (df['MACD_12_26_9'].iloc[-1] > df['MACDs_12_26_9'].iloc[-1])
        macd_bear_cross = (df['MACD_12_26_9'].iloc[-2] > df['MACDs_12_26_9'].iloc[-2]) and \
                          (df['MACD_12_26_9'].iloc[-1] < df['MACDs_12_26_9'].iloc[-1])
        
        # Price near support/resistance
        near_support = (last_close - last_lower_band) / last_close < 0.03
        near_resistance = (last_upper_band - last_close) / last_close < 0.03
        
        # Trend strength using ADX
        df['adx'] = ta.adx(df['High'], df['Low'], df['Close'])['ADX_14']
        strong_trend = df['adx'].iloc[-1] > 25
        
        # Calculate returns
        df['daily_return'] = df['Close'].pct_change() * 100
        recent_performance = df['daily_return'].tail(5).mean()
        
        # Calculate volume trend
        df['volume_ma'] = ta.sma(df['Volume'], length=20)
        volume_trend = df['Volume'].iloc[-1] > df['volume_ma'].iloc[-1]
        
        # Return the technical indicators and their values
        return {
            "rsi": df['rsi'].iloc[-1],
            "macd": df['MACD_12_26_9'].iloc[-1],
            "macd_signal": df['MACDs_12_26_9'].iloc[-1],
            "macd_histogram": df['MACDh_12_26_9'].iloc[-1],
            "ma_short": df['ma_short'].iloc[-1],
            "ma_long": df['ma_long'].iloc[-1],
            "upper_band": last_upper_band,
            "lower_band": last_lower_band,
            "adx": df['adx'].iloc[-1],
            "volatility": volatility,
            "recent_performance": recent_performance,
            
            "is_uptrend": uptrend,
            "is_overbought": overbought,
            "is_oversold": oversold,
            "macd_bullish_cross": macd_bull_cross,
            "macd_bearish_cross": macd_bear_cross,
            "near_support": near_support,
            "near_resistance": near_resistance,
            "strong_trend": strong_trend,
            "high_volume": volume_trend
        }
    except Exception as e:
        print(f"Error calculating technical indicators: {e}")
        return {}

def analyze_technical(technical_indicators):
    """
    Analyze technical indicators to produce a score.
    
    Args:
        technical_indicators (dict): Technical indicators
    
    Returns:
        float: Technical analysis score (0-10)
    """
    if not technical_indicators:
        return 0.0
    
    try:
        score = 5.0  # Neutral starting point
        
        # RSI Analysis
        rsi = technical_indicators.get("rsi", 50)
        if rsi < 30:  # Oversold
            score += 1.0
        elif rsi > 70:  # Overbought
            score -= 1.0
            
        # MACD Analysis
        if technical_indicators.get("macd_bullish_cross", False):
            score += 1.0
        if technical_indicators.get("macd_bearish_cross", False):
            score -= 1.0
            
        # Trend Analysis
        if technical_indicators.get("is_uptrend", False):
            score += 0.75
        else:
            score -= 0.75
            
        # Support/Resistance
        if technical_indicators.get("near_support", False):
            score += 0.5
        if technical_indicators.get("near_resistance", False):
            score -= 0.5
            
        # ADX (Trend Strength)
        adx = technical_indicators.get("adx", 0)
        if adx > 25:  # Strong trend
            if technical_indicators.get("is_uptrend", False):
                score += 0.5
            else:
                score -= 0.5
                
        # Recent Performance
        recent_perf = technical_indicators.get("recent_performance", 0)
        if recent_perf > 0:
            score += 0.25 * min(recent_perf, 2)  # Cap at 0.5
        else:
            score -= 0.25 * min(abs(recent_perf), 2)  # Cap at 0.5
            
        # Volume
        if technical_indicators.get("high_volume", False):
            if technical_indicators.get("is_uptrend", False):
                score += 0.5
            else:
                score -= 0.5
        
        # Ensure the score is within bounds
        return max(0, min(score, 10))
    except Exception as e:
        print(f"Error analyzing technical indicators: {e}")
        return 5.0  # Return neutral score on error
