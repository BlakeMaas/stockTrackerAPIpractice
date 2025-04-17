# main.py
import streamlit as st
from utils import fetch_daily_stock_data
import pandas as pd
import os

# --- Set config (must be first!) ---
st.set_page_config(page_title="Stock Tracker", layout="centered")

# --- THEME TOGGLE ---
theme = st.radio("Choose Theme", ["Light", "Dark"], horizontal=True)

# --- Apply custom CSS based on theme ---
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

# --- App Title ---
st.title("📈 Stock Tracker")

# --- User Input ---
symbol = st.text_input("Enter a stock symbol (e.g., AAPL)", value="AAPL")

# --- Fetch & Display Data ---
if symbol:
    raw_data = fetch_daily_stock_data(symbol)

    # Show raw API response (for debugging)
    st.write("🔍 Raw API Response:", raw_data)

    # Handle different possible responses
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
        st.warning("⚠️ You're hitting the API rate limit. Try again in 60 seconds.")

    elif "Error Message" in raw_data:
        st.error(f"❌ Alpha Vantage error: {raw_data['Error Message']}")

    else:
        st.error("❌ Unknown error. Please check your API key and stock symbol.")
