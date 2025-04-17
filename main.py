# main.py
import streamlit as st
from utils import fetch_daily_stock_data
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Stock Tracker", layout="centered")

# --- Simulated Theme Toggle (informational only) ---
theme = st.radio("Choose Theme", ["Dark", "Light"], horizontal=True)
st.caption("⚠️ Theme changes require browser refresh to fully apply.")

# --- APP TITLE ---
st.title("📈 Stock Tracker")

# --- User Input ---
symbol = st.text_input("Enter a stock symbol (e.g., AAPL)", value="AAPL")

# --- Fetch and Display Data ---
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

    elif "Note" in raw_data:
        st.warning("⚠️ API rate limit exceeded. Try again in about 60 seconds.")
    elif "Error Message" in raw_data:
        st.error(f"❌ Invalid symbol or API call: {raw_data['Error Message']}")
    elif "Information" in raw_data:
        st.warning("ℹ️ Info from API: Request limit reached or invalid key.")
    else:
        st.error("❌ Failed to fetch data. Please check the symbol or your API key.")
