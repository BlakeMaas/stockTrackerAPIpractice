# main.py
import streamlit as st
from utils import fetch_daily_stock_data
import pandas as pd
import os

# --- Must be first! ---
st.set_page_config(page_title="Stock Tracker", layout="centered")

# Optional: Debug API key loading
st.text(f"API Key Present: {bool(os.getenv('ALPHA_VANTAGE_API_KEY'))}")

# --- THEME TOGGLE ---
theme = st.radio("Choose Theme", ["Light", "Dark"], horizontal=True)
...

# --- Apply CSS based on theme selection ---
if theme == "Dark":
    st.markdown("""
        <style>
            body, .stApp {
                background-color: #0e1117;
                color: #fafafa;
            }
            .stRadio > label, .stRadio div {
                color: #fafafa !important;
            }
            .stButton>button {
                background-color: #262730;
                color: #fafafa;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            body, .stApp {
                background-color: #ffffff;
                color: #000000;
            }
            .stRadio > label, .stRadio div {
                color: #000000 !important;
            }
            .stButton>button {
                background-color: #f0f2f6;
                color: #000000;
            }
        </style>
    """, unsafe_allow_html=True)

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
    else:
        st.error("Failed to fetch data. Please check the symbol.")
