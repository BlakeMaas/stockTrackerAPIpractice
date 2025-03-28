# Streamlit Stock Tracker

This is a simple Streamlit app that allows users to search for a stock symbol (like `AAPL` or `TSLA`) and view historical price data using the Alpha Vantage API.

## Features
- Live stock data (Daily OHLC)
- Chart and table views
- Built with Streamlit
- Deployed on Streamlit Community Cloud

## Setup
1. Clone the repo
2. Install requirements: `pip install -r requirements.txt`
3. Add your API key to `.streamlit/secrets.toml`:
```toml
ALPHA_VANTAGE_API_KEY = "your-key-here"
