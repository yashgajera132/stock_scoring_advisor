import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from modules.stock_data import get_stock_data, get_company_info, get_fundamental_data
from modules.technical import calculate_technical_indicators, analyze_technical
from modules.fundamental import analyze_fundamental
from modules.news import get_news, analyze_sentiment
from modules.scoring import calculate_overall_score, get_score_components
from modules.advisory import get_investment_advice
from utils.helpers import format_large_number, format_percentage, validate_ticker
from utils.visualize import (
    plot_stock_price, 
    plot_technical_indicators,
    plot_score_gauge,
    create_sentiment_distribution_chart
)
import config

# Set page config
st.set_page_config(page_title="Stock Scoring & Advisory Dashboard", layout="wide", page_icon="📊")

# Add custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem 1rem;
        max-width: 1200px;
    }
    .ticker-input {
        font-size: 1.2rem;
        padding: 0.5rem;
    }
    .score-card {
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .advice-card {
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-top: 1rem;
    }
    .news-item {
        padding: 1rem;
        border-bottom: 1px solid #eee;
    }
    .news-title {
        font-weight: bold;
        font-size: 1.1rem;
    }
    .news-source {
        color: #555;
        font-size: 0.8rem;
    }
    .sentiment-positive {
        color: green;
    }
    .sentiment-negative {
        color: red;
    }
    .sentiment-neutral {
        color: gray;
    }
    .header-container {
        display: flex;
        align-items: center;
    }
    .subheader {
        color: #555;
        font-size: 1.2rem;
    }
    .stock-info {
        padding: 1rem;
        background: #f9f9f9;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("Stock Scoring & Advisory Dashboard")
st.markdown("Enter a stock symbol to get analysis, scoring, and investment advice.")

# Sidebar
st.sidebar.header("Settings")
time_period = st.sidebar.selectbox(
    "Select Time Period",
    options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
    index=3  # Default to 1y
)

# Main form
with st.form("stock_form"):
    ticker_input = st.text_input("Enter Stock Symbol (e.g., AAPL, TCS.NS):", key="ticker")
    submit_button = st.form_submit_button("Analyze Stock")

# Process the form
if submit_button and ticker_input:
    ticker = ticker_input.strip().upper()
    
    # Validate ticker
    with st.spinner(f"Validating ticker {ticker}..."):
        is_valid = validate_ticker(ticker)
    
    if not is_valid:
        st.error(f"Invalid ticker symbol: {ticker}. Please enter a valid stock symbol.")
    else:
        # Show a progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Get stock data
        status_text.text("Fetching stock data...")
        stock_data = get_stock_data(ticker, period=time_period)
        company_info = get_company_info(ticker)
        progress_bar.progress(20)
        
        # Step 2: Get fundamental data
        status_text.text("Analyzing fundamentals...")
        fundamental_data = get_fundamental_data(ticker)
        progress_bar.progress(30)
        
        # Step 3: Calculate technical indicators
        status_text.text("Calculating technical indicators...")
        technical_indicators = calculate_technical_indicators(stock_data)
        progress_bar.progress(40)
        
        # Step 4: Get news and analyze sentiment
        status_text.text("Fetching recent news and analyzing sentiment...")
        news_articles = get_news(ticker, company_info.get("name"))
        news_sentiment = analyze_sentiment(news_articles)
        progress_bar.progress(60)
        
        # Step 5: Calculate scores
        status_text.text("Calculating scores...")
        technical_score = analyze_technical(technical_indicators)
        fundamental_score = analyze_fundamental(fundamental_data)
        sentiment_score = news_sentiment.get("sentiment_score", 5.0)
        overall_score = calculate_overall_score(technical_score, fundamental_score, sentiment_score)
        score_components = get_score_components(technical_indicators, fundamental_data, news_sentiment)
        progress_bar.progress(80)
        
        # Step 6: Get investment advice
        status_text.text("Generating investment advice...")
        advice = get_investment_advice(overall_score, technical_indicators, fundamental_data, news_sentiment)
        progress_bar.progress(100)
        
        # Clear status messages
        status_text.empty()
        progress_bar.empty()
        
        # Display results
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Company info
            if company_info:
                st.subheader(f"{company_info.get('name', ticker)} ({ticker})")
                st.markdown(f"Sector: {company_info.get('sector', 'N/A')} | Industry: {company_info.get('industry', 'N/A')} | Market Cap: {format_large_number(company_info.get('market_cap', 'N/A'))}")
            else:
                st.subheader(f"{ticker}")
            
            # Stock price chart
            st.subheader("Price History")
            price_chart = plot_stock_price(stock_data, time_period)
            st.plotly_chart(price_chart, use_container_width=True)
            
            # Technical indicators
            st.subheader("Technical Analysis")
            tech_chart = plot_technical_indicators(stock_data)
            if tech_chart:
                st.plotly_chart(tech_chart, use_container_width=True)
            
        with col2:
            # Score gauge
            st.plotly_chart(plot_score_gauge(overall_score), use_container_width=True)
            
            # Investment advice
            st.markdown(f"### Recommendation: {advice['recommendation']}")
            for point in advice['rationale']:
                st.write(f"• {point}")
            
            # Component scores
            st.subheader("Score Components")
            col_tech, col_fund, col_news = st.columns(3)
            with col_tech:
                st.metric("Technical", f"{technical_score:.1f}/10")
            with col_fund:
                st.metric("Fundamental", f"{fundamental_score:.1f}/10")
            with col_news:
                st.metric("News Sentiment", f"{sentiment_score:.1f}/10")
                
        # News sentiment
        st.subheader("Recent News & Sentiment")
        col_news1, col_news2 = st.columns([3, 1])
        
        with col_news1:
            if news_articles:
                for i, article in enumerate(news_sentiment.get("articles", [])[:5]):  # Show top 5 articles
                    sentiment_class = f"sentiment-{article['sentiment']}"
                    
                    st.markdown(f"""
                    <div class="news-item">
                        <a href="{article['url']}" target="_blank" class="news-title">{article['title']}</a>
                        <div class="news-source">Source: {article['source']} | 
                            <span class="{sentiment_class}">Sentiment: {article['sentiment'].title()} 
                            ({article['sentiment_score']:.2f})</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No recent news found for this stock")
        
        with col_news2:
            if news_articles:
                sentiment_chart = create_sentiment_distribution_chart(news_sentiment)
                st.plotly_chart(sentiment_chart, use_container_width=True)
                
        # Detailed metrics
        with st.expander("View Detailed Metrics"):
            col_tech_details, col_fund_details = st.columns(2)
            
            with col_tech_details:
                st.subheader("Technical Indicators")
                tech_df = pd.DataFrame([
                    {"Metric": "RSI (14)", "Value": f"{technical_indicators.get('rsi', 'N/A'):.2f}", 
                     "Status": "Oversold" if technical_indicators.get('rsi', 50) < 30 else 
                              "Overbought" if technical_indicators.get('rsi', 50) > 70 else "Neutral"},
                    {"Metric": "MACD", "Value": f"{technical_indicators.get('macd', 'N/A'):.4f}",
                     "Status": "Above Signal" if technical_indicators.get('macd', 0) > technical_indicators.get('macd_signal', 0) 
                              else "Below Signal"},
                    {"Metric": "Trend", "Value": "Uptrend" if technical_indicators.get('is_uptrend', False) else "Downtrend",
                     "Status": "Strong" if technical_indicators.get('strong_trend', False) else "Average"},
                    {"Metric": "Volatility", "Value": f"{technical_indicators.get('volatility', 'N/A'):.2f}%",
                     "Status": "High" if technical_indicators.get('volatility', 2) > 3 else 
                              "Low" if technical_indicators.get('volatility', 2) < 1 else "Average"},
                ])
                st.table(tech_df)
            
            with col_fund_details:
                st.subheader("Fundamental Metrics")
                fund_df = pd.DataFrame([
                    {"Metric": "P/E Ratio", "Value": f"{fundamental_data.get('trailing_pe', 'N/A')}" if fundamental_data.get('trailing_pe') is not None else "N/A"},
                    {"Metric": "EPS", "Value": f"{fundamental_data.get('eps', 'N/A')}" if fundamental_data.get('eps') is not None else "N/A"},
                    {"Metric": "ROE", "Value": f"{format_percentage(fundamental_data.get('roe'))}"},
                    {"Metric": "Debt to Equity", "Value": f"{fundamental_data.get('debt_to_equity', 'N/A')}" if fundamental_data.get('debt_to_equity') is not None else "N/A"},
                    {"Metric": "Profit Margin", "Value": f"{format_percentage(fundamental_data.get('profit_margins'))}"},
                    {"Metric": "Dividend Yield", "Value": f"{format_percentage(fundamental_data.get('dividend_yield'))}"},
                ])
                st.table(fund_df)
else:
    # When the app first loads or if no ticker is submitted
    st.info("Enter a stock symbol and click 'Analyze Stock' to get started.")
    
    # Example stocks
    st.markdown("### Example stocks to try:")
    examples = {
        "US Tech": "AAPL, MSFT, GOOGL, AMZN, META",
        "US Financial": "JPM, BAC, GS, V, MA",
        "Indian": "TCS.NS, RELIANCE.NS, HDFCBANK.NS, INFY.NS",
        "European": "SAP.DE, ASML.AS, LVMH.PA, NOVO-B.CO"
    }
    
    for category, stocks in examples.items():
        st.markdown(f"**{category}**: {stocks}")

# Footer
st.markdown("---")
st.markdown("Stock Scoring & Advisory Dashboard - Data provided by Yahoo Finance") 