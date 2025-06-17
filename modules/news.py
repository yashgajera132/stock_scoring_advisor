import requests
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sys
import os
import pandas as pd
import time
import re

# Add the project root directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def get_news(ticker, company_name=None, days=7):
    """
    Fetch recent news articles about a stock.
    
    Args:
        ticker (str): Stock ticker symbol
        company_name (str, optional): Company name for better search results
        days (int): Number of days to look back
    
    Returns:
        list: List of news articles with title, url, published date, and source
    """
    try:
        # Use company name if provided, otherwise use ticker
        query = company_name if company_name else ticker
        
        # Format dates
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Format dates for NewsAPI
        from_date = start_date.strftime('%Y-%m-%d')
        to_date = end_date.strftime('%Y-%m-%d')
        
        # Get news from NewsAPI
        url = f"https://newsapi.org/v2/everything"
        params = {
            'q': f'"{query}" OR "{ticker}"',
            'from': from_date,
            'to': to_date,
            'language': 'en',
            'sortBy': 'publishedAt',
            'apiKey': config.NEWSAPI_KEY
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            
            # Extract relevant information
            news_list = []
            for article in articles[:10]:  # Limit to top 10 articles
                news_item = {
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'published_at': article.get('publishedAt', ''),
                    'source': article.get('source', {}).get('name', '')
                }
                news_list.append(news_item)
                
            return news_list
        else:
            print(f"Error fetching news. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def analyze_sentiment(news_articles):
    """
    Analyze sentiment of news articles.
    
    Args:
        news_articles (list): List of news articles
    
    Returns:
        dict: Sentiment analysis results
    """
    if not news_articles:
        return {
            "articles": [],
            "average_sentiment": 0,
            "sentiment_score": 5.0,  # Neutral score
            "positive": 0,
            "negative": 0,
            "neutral": 0
        }
    
    try:
        analyzer = SentimentIntensityAnalyzer()
        
        # Analyze sentiment of each article
        sentiment_results = []
        compound_scores = []
        positive, negative, neutral = 0, 0, 0
        
        for article in news_articles:
            # Combine title and description for better sentiment analysis
            text = f"{article['title']} {article['description']}"
            
            vs = analyzer.polarity_scores(text)
            compound = vs['compound']
            
            # Determine sentiment category
            if compound >= 0.05:
                sentiment = "positive"
                positive += 1
            elif compound <= -0.05:
                sentiment = "negative"
                negative += 1
            else:
                sentiment = "neutral"
                neutral += 1
                
            # Store results
            article_with_sentiment = {
                'title': article['title'],
                'url': article['url'],
                'published_at': article['published_at'],
                'source': article['source'],
                'sentiment': sentiment,
                'sentiment_score': compound
            }
            
            sentiment_results.append(article_with_sentiment)
            compound_scores.append(compound)
        
        # Calculate average sentiment
        avg_sentiment = sum(compound_scores) / len(compound_scores) if compound_scores else 0
        
        # Convert to a 0-10 score
        # Map from [-1, 1] to [0, 10]
        sentiment_score = 5 + (avg_sentiment * 5)
        
        return {
            "articles": sentiment_results,
            "average_sentiment": avg_sentiment,
            "sentiment_score": sentiment_score,
            "positive": positive,
            "negative": negative,
            "neutral": neutral
        }
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return {
            "articles": [],
            "average_sentiment": 0,
            "sentiment_score": 5.0,  # Neutral score
            "positive": 0,
            "negative": 0,
            "neutral": 0
        }
