import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import re

def format_large_number(num):
    """Format large numbers in a readable way (e.g., 1.2B, 345.8M)."""
    if num is None:
        return "N/A"
        
    abs_num = abs(num)
    sign = "-" if num < 0 else ""
    
    if abs_num >= 1e12:
        return f"{sign}{abs_num / 1e12:.2f}T"
    elif abs_num >= 1e9:
        return f"{sign}{abs_num / 1e9:.2f}B"
    elif abs_num >= 1e6:
        return f"{sign}{abs_num / 1e6:.2f}M"
    elif abs_num >= 1e3:
        return f"{sign}{abs_num / 1e3:.2f}K"
    else:
        return f"{sign}{abs_num:.2f}"

def format_percentage(value):
    """Format value as percentage."""
    if value is None:
        return "N/A"
    
    return f"{value * 100:.2f}%"

def validate_ticker(ticker):
    """Check if a ticker is valid."""
    try:
        # Basic format check
        if not ticker or not isinstance(ticker, str):
            return False
            
        # Remove any whitespace
        ticker = ticker.strip().upper()
        
        # Check if ticker has valid format
        if not re.match(r'^[A-Z0-9\.\-]+$', ticker):
            return False
            
        # Try to fetch some minimal data from yfinance
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Check if we got valid info
        if 'regularMarketPrice' not in info and 'currentPrice' not in info:
            return False
            
        return True
    except:
        return False

def get_date_range(period='1y'):
    """Convert period to start and end dates."""
    end_date = datetime.now()
    
    if period == '1d':
        start_date = end_date - timedelta(days=1)
    elif period == '5d':
        start_date = end_date - timedelta(days=5)
    elif period == '1mo':
        start_date = end_date - timedelta(days=30)
    elif period == '3mo':
        start_date = end_date - timedelta(days=90)
    elif period == '6mo':
        start_date = end_date - timedelta(days=180)
    elif period == '1y':
        start_date = end_date - timedelta(days=365)
    elif period == '2y':
        start_date = end_date - timedelta(days=2*365)
    elif period == '5y':
        start_date = end_date - timedelta(days=5*365)
    else:  # Default to 1 year
        start_date = end_date - timedelta(days=365)
        
    return start_date, end_date
    