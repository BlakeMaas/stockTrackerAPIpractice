
# main.py
import streamlit as st
from utils import fetch_daily_stock_data
import pandas as pd

st.set_page_config(page_title="Stock Tracker", layout="centered")
st.title("Stock Tracker")

symbol = st.text_input("Enter a stock symbol (e.g., AAPL)", value="AAPL")

if symbol:
    raw_data = fetch_daily_stock_data(symbol)

    if "Time Series (Daily)" in raw_data:
        ts = raw_data["Time Series (Daily)"]
        df = pd.DataFrame(ts).T
        df.index = pd.to_datetime(df.index)
        df = df.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        })
        df = df.astype(float)
        st.line_chart(df["Close"])
        st.dataframe(df.head(10))
    else:
        st.error("Failed to fetch data. Please check the symbol.")