# tests/test_utils.py
from utils import fetch_daily_stock_data

def test_fetch_daily_stock_data_structure():
    data = fetch_daily_stock_data("AAPL")
    assert "Meta Data" in data
    assert "Time Series (Daily)" in data

