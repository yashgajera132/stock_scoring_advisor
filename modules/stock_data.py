import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add the project root directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def get_stock_data(ticker, period=config.DEFAULT_PERIOD, interval=config.DEFAULT_INTERVAL):
    """
    Fetch stock price data using yfinance.
    
    Args:
        ticker (str): Stock ticker symbol
        period (str): Data period (e.g. '1d', '5d', '1mo', '3mo', '1y', '5y', 'max')
        interval (str): Data interval (e.g. '1m', '5m', '15m', '1d', '1wk', '1mo', '3mo')
    
    Returns:
        pd.DataFrame: DataFrame with stock price data
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        
        if df.empty:
            raise ValueError(f"No data found for ticker: {ticker}")
        
        return df
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return pd.DataFrame()

def get_company_info(ticker):
    """
    Fetch company information.
    
    Args:
        ticker (str): Stock ticker symbol
    
    Returns:
        dict: Company information
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Extract relevant info
        company_info = {
            "name": info.get("longName", ""),
            "sector": info.get("sector", ""),
            "industry": info.get("industry", ""),
            "website": info.get("website", ""),
            "market_cap": info.get("marketCap", None),
            "country": info.get("country", ""),
            "currency": info.get("currency", ""),
            "exchange": info.get("exchange", "")
        }
        
        return company_info
    except Exception as e:
        print(f"Error fetching company info: {e}")
        return {}

def get_fundamental_data(ticker):
    """
    Fetch fundamental data for a stock.
    
    Args:
        ticker (str): Stock ticker symbol
    
    Returns:
        dict: Fundamental metrics
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        fundamental_data = {
            "trailing_pe": info.get("trailingPE", None),
            "forward_pe": info.get("forwardPE", None),
            "price_to_book": info.get("priceToBook", None),
            "eps": info.get("trailingEps", None),
            "roe": info.get("returnOnEquity", None),
            "profit_margins": info.get("profitMargins", None),
            "dividend_yield": info.get("dividendYield", None),
            "debt_to_equity": info.get("debtToEquity", None),
            "current_ratio": info.get("currentRatio", None),
            "quick_ratio": info.get("quickRatio", None),
            "beta": info.get("beta", None)
        }
        
        return fundamental_data
    except Exception as e:
        print(f"Error fetching fundamental data: {e}")
        return {}
