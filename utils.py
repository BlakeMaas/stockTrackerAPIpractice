# utils.py
import requests
import streamlit as st
import os

def fetch_daily_stock_data(symbol: str) -> dict:
    """Fetches daily stock data from Alpha Vantage."""
    
api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
if not api_key:
    raise RuntimeError("Missing ALPHA_VANTAGE_API_KEY environment variable")

    url = (
        "https://www.alphavantage.co/query?"
        f"function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&outputsize=compact"
    )

    response = requests.get(url)
    data = response.json()
    return data

