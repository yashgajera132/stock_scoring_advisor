import os

# API keys
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "3d8f441bd03b4c189ad1e73d81d83ced")

# Stock data parameters
DEFAULT_PERIOD = "1y"
DEFAULT_INTERVAL = "1d"

# Technical analysis parameters
RSI_WINDOW = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
MA_SHORT = 50
MA_LONG = 200

# Scoring weights
TECHNICAL_WEIGHT = 0.4
FUNDAMENTAL_WEIGHT = 0.4
NEWS_SENTIMENT_WEIGHT = 0.2

# Advisory thresholds
BUY_THRESHOLD = 7.0
SELL_THRESHOLD = 4.0
HOLD_THRESHOLD = 5.5
