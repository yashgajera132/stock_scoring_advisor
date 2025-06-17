import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import yfinance as yf
import streamlit as st

def plot_stock_price(data, period):
    """
    Plot stock price history with volume.
    
    Args:
        data (pd.DataFrame): Stock price data
        period (str): Time period for the plot title
    
    Returns:
        plotly.graph_objects.Figure: Plotly figure
    """
    # Check if data is empty or missing required columns
    if data.empty or not all(col in data.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume']):
        st.error("Stock data is missing or incomplete. Please check the data source.")
        return None

    # Create figure with secondary y-axis (for volume)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                       vertical_spacing=0.05, 
                       row_heights=[0.7, 0.3])
    
    # Add candlestick chart for price
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name="Price"
        ),
        row=1, col=1
    )
    
    # Add volume bar chart
    colors = ['red' if row['Open'] > row['Close'] else 'green' for _, row in data.iterrows()]
    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data['Volume'],
            marker_color=colors,
            name="Volume"
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        title=f"Stock Price History ({period})",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        template="plotly_white",
        height=600,
    )
    
    # Update y-axis labels
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    
    return fig

def plot_technical_indicators(data):
    """
    Plot technical indicators (RSI, MACD).
    
    Args:
        data (pd.DataFrame): DataFrame with technical indicators
    
    Returns:
        plotly.graph_objects.Figure: Plotly figure
    """
    # Check that we have technical indicators in the data
    if 'rsi' not in data.columns or 'MACD_12_26_9' not in data.columns:
        return None
    
    # Create figure with three subplots
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                       vertical_spacing=0.05,
                       row_heights=[0.5, 0.25, 0.25])
    
    # Add price line
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            name="Close Price"
        ),
        row=1, col=1
    )
    
    # Add moving averages if they exist
    if 'ma_short' in data.columns and 'ma_long' in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['ma_short'],
                mode='lines',
                line=dict(width=1, color='blue'),
                name=f"{config.MA_SHORT}-day MA"
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['ma_long'],
                mode='lines',
                line=dict(width=1, color='red'),
                name=f"{config.MA_LONG}-day MA"
            ),
            row=1, col=1
        )
    
    # Add RSI
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['rsi'],
            mode='lines',
            name="RSI",
            line=dict(color='purple')
        ),
        row=2, col=1
    )
    
    # Add RSI overbought/oversold lines
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=[70] * len(data),
            mode='lines',
            line=dict(color='red', width=1, dash='dash'),
            name="Overbought"
        ),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=[30] * len(data),
            mode='lines',
            line=dict(color='green', width=1, dash='dash'),
            name="Oversold"
        ),
        row=2, col=1
    )
    
    # Add MACD
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['MACD_12_26_9'],
            mode='lines',
            name="MACD",
            line=dict(color='blue')
        ),
        row=3, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['MACDs_12_26_9'],
            mode='lines',
            name="MACD Signal",
            line=dict(color='red')
        ),
        row=3, col=1
    )
    
    # MACD histogram
    colors = ['red' if val < 0 else 'green' for val in data['MACDh_12_26_9']]
    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data['MACDh_12_26_9'],
            name="MACD Histogram",
            marker_color=colors
        ),
        row=3, col=1
    )
    
    # Update layout
    fig.update_layout(
        title="Technical Indicators",
        template="plotly_white",
        height=800,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Update y-axis labels
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="RSI", row=2, col=1)
    fig.update_yaxes(title_text="MACD", row=3, col=1)
    
    return fig

def plot_score_gauge(score):
    """
    Create a gauge chart to visualize the overall score.
    
    Args:
        score (float): Score value (0-10)
    
    Returns:
        plotly.graph_objects.Figure: Plotly figure
    """
    # Define gauge colors
    if score >= 7:
        color = "green"
    elif score >= 5:
        color = "yellow"
    else:
        color = "red"
    
    # Create gauge chart
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        title = {'text': "Stock Score"},
        gauge = {
            'axis': {'range': [None, 10]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 4], 'color': "lightgray"},
                {'range': [4, 7], 'color': "gray"},
                {'range': [7, 10], 'color': "darkgray"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    
    return fig

def create_sentiment_distribution_chart(news_sentiment):
    """
    Create a pie chart showing distribution of sentiment in news.
    
    Args:
        news_sentiment (dict): News sentiment data
    
    Returns:
        plotly.graph_objects.Figure: Plotly figure
    """
    labels = ['Positive', 'Neutral', 'Negative']
    values = [
        news_sentiment.get('positive', 0),
        news_sentiment.get('neutral', 0),
        news_sentiment.get('negative', 0)
    ]
    
    # Add small value to prevent empty chart
    if sum(values) == 0:
        values = [1, 1, 1]
    
    colors = ['green', 'gray', 'red']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.3,
        marker_colors=colors
    )])
    
    fig.update_layout(title_text="News Sentiment Distribution")
    
    return fig
