# tests/test_utils.py
from utils import fetch_daily_stock_data
import os

import os

api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

if not api_key:
    raise RuntimeError("Missing ALPHA_VANTAGE_API_KEY environment variable")


def test_fetch_daily_stock_data_structure():
    data = fetch_daily_stock_data("AAPL")
    assert "Meta Data" in data
    assert "Time Series (Daily)" in data

