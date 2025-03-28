# utils.py
import requests
import streamlit as st

def fetch_daily_stock_data(symbol: str) -> dict:
    """Fetches daily stock data from Alpha Vantage."""
    api_key = st.secrets["ALPHA_VANTAGE_API_KEY"]
    url = (
        "https://www.alphavantage.co/query?"
        f"function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&outputsize=compact"
    )

    response = requests.get(url)
    data = response.json()
    return data

