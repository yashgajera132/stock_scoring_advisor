# Stock Scoring & Advisory System 📈

A comprehensive stock analysis and advisory system that provides detailed insights into stocks through technical analysis, fundamental analysis, and news sentiment analysis.

## 🌟 Features

### 1. Stock Data Analysis
- Real-time stock price data retrieval
- Historical price analysis
- Volume analysis
- Interactive price charts with candlestick patterns

### 2. Technical Analysis
- Moving Averages (SMA, EMA)
- Relative Strength Index (RSI)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- Volume analysis
- Trend analysis

### 3. Fundamental Analysis
- Company Overview
- Financial Ratios
- Growth Metrics
- Profitability Analysis
- Market Performance
- Key Financial Indicators

### 4. News Sentiment Analysis
- Real-time news aggregation
- Sentiment scoring
- News impact analysis
- Market sentiment trends
- News categorization

### 5. Investment Advisory
- Comprehensive stock scoring
- Investment recommendations
- Risk assessment
- Market trend analysis
- Portfolio optimization suggestions

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yashgajera132/stock_scoring_advisor.git
cd stock_scoring_advisor
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up API keys:
   - Create a `.env` file in the root directory
   - Add your API keys:
     ```
     NEWS_API_KEY=your_news_api_key
     ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
     ```

## 💻 Usage

### Running the Dashboard
```bash
streamlit run dashboard.py
```

### Running the Frontend
```bash
streamlit run frontend.py
```

### Running the Basic App
```bash
streamlit run app.py
```

## 📊 Features in Detail

### Stock Analysis
- Real-time price updates
- Historical data analysis
- Volume analysis
- Price trend visualization
- Technical indicator calculations

### Technical Indicators
- Moving Averages (SMA, EMA)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- Volume analysis
- Support and resistance levels

### Fundamental Analysis
- Company information
- Financial ratios
- Growth metrics
- Market performance
- Key financial indicators
- Industry comparison

### News Analysis
- Real-time news updates
- Sentiment analysis
- News impact assessment
- Market sentiment trends
- News categorization
- Historical news analysis

### Investment Advisory
- Comprehensive stock scoring
- Investment recommendations
- Risk assessment
- Market trend analysis
- Portfolio optimization
- Investment strategy suggestions

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Plotly
- **Stock Data**: yfinance
- **News API**: NewsAPI
- **Sentiment Analysis**: VADER
- **Technical Analysis**: TA-Lib

## 📈 Project Structure

```
stock_scoring_advisor/
├── app.py                 # Main application file
├── dashboard.py           # Production dashboard
├── frontend.py            # Frontend interface
├── config.py             # Configuration settings
├── requirements.txt      # Project dependencies
├── modules/             # Core functionality modules
│   ├── stock_data.py    # Stock data handling
│   ├── technical.py     # Technical analysis
│   ├── fundamental.py   # Fundamental analysis
│   ├── news.py         # News analysis
│   ├── scoring.py      # Scoring system
│   └── advisory.py     # Investment advisory
└── utils/              # Utility functions
    ├── helpers.py      # Helper functions
    └── visualize.py    # Visualization utilities
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Yash Gajera** - *Initial work* - [yashgajera132](https://github.com/yashgajera132)

## 🙏 Acknowledgments

- Thanks to all the open-source libraries and tools that made this project possible
- Special thanks to the financial data providers and API services
- Appreciation to the Streamlit community for their excellent documentation

## 📞 Contact

For any queries or suggestions, please reach out to:
- GitHub: [yashgajera132](https://github.com/yashgajera132)

## 🔄 Updates

### Latest Updates
- Added comprehensive technical analysis
- Implemented news sentiment analysis
- Enhanced visualization capabilities
- Added production-level dashboard
- Improved user interface and experience

### Planned Features
- Portfolio management
- Real-time alerts
- Advanced technical indicators
- Machine learning predictions
- Mobile application
